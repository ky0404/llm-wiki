"""API 主入口 - 配置化、进程管理优化、Watcher 改造"""
import os
import sys
import signal
import logging
import threading
import asyncio
import subprocess
import multiprocessing
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json

from config import config


logger = config.get_logger(__name__)

WATCHDOG_AVAILABLE = False
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    logger.warning("watchdog not installed, using polling fallback")


class ProcessManager:
    """进程管理器 - 健壮的进程生命周期管理"""

    def __init__(self):
        self.processes: dict = {}
        self._shutdown_event = threading.Event()

    def start_process(self, name: str, cmd: list, cwd: str = None, env: dict = None):
        """启动子进程，带日志记录"""
        if name in self.processes and self.processes[name].poll() is None:
            logger.warning(f"[ProcessManager] 进程 {name} 已在运行")
            return

        full_env = os.environ.copy()
        if env:
            full_env.update(env)

        try:
            process = subprocess.Popen(
                cmd,
                cwd=cwd,
                env=full_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            self.processes[name] = process
            logger.info(f"[ProcessManager] 启动进程 {name} (PID: {process.pid})")

            stdout_thread = threading.Thread(
                target=self._stream_log,
                args=(f"{name}_stdout", process.stdout),
                daemon=True
            )
            stdout_thread.start()

            stderr_thread = threading.Thread(
                target=self._stream_log,
                args=(f"{name}_stderr", process.stderr),
                daemon=True
            )
            stderr_thread.start()

        except Exception as e:
            logger.error(f"[ProcessManager] 启动进程 {name} 失败: {e}")
            raise

    def _stream_log(self, name: str, stream):
        """流式日志输出"""
        try:
            for line in iter(stream.readline, ''):
                if line:
                    logger.info(f"[{name}] {line.rstrip()}")
        except Exception as e:
            logger.debug(f"[{name}] 流读取结束: {e}")

    def stop_process(self, name: str, timeout: int = 10):
        """优雅停止进程"""
        if name not in self.processes:
            logger.warning(f"[ProcessManager] 进程 {name} 不存在")
            return

        process = self.processes[name]
        if process.poll() is not None:
            logger.info(f"[ProcessManager] 进程 {name} 已退出")
            del self.processes[name]
            return

        logger.info(f"[ProcessManager] 停止进程 {name} (PID: {process.pid})")
        process.terminate()

        try:
            process.wait(timeout=timeout)
            logger.info(f"[ProcessManager] 进程 {name} 已优雅退出")
        except subprocess.TimeoutExpired:
            logger.warning(f"[ProcessManager] 进程 {name} 优雅退出超时，强制杀死")
            process.kill()
            process.wait()
            logger.info(f"[ProcessManager] 进程 {name} 已强制杀死")

        del self.processes[name]

    def stop_all(self):
        """停止所有进程"""
        logger.info("[ProcessManager] 停止所有子进程")
        for name in list(self.processes.keys()):
            self.stop_process(name)

    def is_running(self, name: str) -> bool:
        """检查进程是否运行"""
        if name not in self.processes:
            return False
        return self.processes[name].poll() is None


process_manager = ProcessManager()


change_queue: asyncio.Queue = None
last_wiki_mtime = 0
last_backup_time = 0
watcher_initialized = False


if WATCHDOG_AVAILABLE:
    class WatchdogHandler(FileSystemEventHandler):
        """Watchdog 文件系统事件处理器"""

        def __init__(self, queue: asyncio.Queue):
            self.queue = queue
            super().__init__()

        def on_modified(self, event):
            if not event.is_directory and event.src_path.endswith(".md"):
                logger.info(f"[Watcher] 文件修改: {event.src_path}")
                asyncio.create_task(self.queue.put({
                    "type": "wiki_change",
                    "event": "modified",
                    "path": event.src_path,
                    "timestamp": asyncio.get_event_loop().time()
                }))

        def on_created(self, event):
            if not event.is_directory and event.src_path.endswith(".md"):
                logger.info(f"[Watcher] 文件创建: {event.src_path}")
                asyncio.create_task(self.queue.put({
                    "type": "wiki_change",
                    "event": "created",
                    "path": event.src_path,
                    "timestamp": asyncio.get_event_loop().time()
                }))

        def on_deleted(self, event):
            if not event.is_directory and event.src_path.endswith(".md"):
                logger.info(f"[Watcher] 文件删除: {event.src_path}")
                asyncio.create_task(self.queue.put({
                    "type": "wiki_change",
                    "event": "deleted",
                    "path": event.src_path,
                    "timestamp": asyncio.get_event_loop().time()
                }))

    async def watchdog_watcher():
        """Watchdog Watcher - 主推模式"""
        global watcher_initialized

        wiki_dir = config.WIKI_DATA_DIR
        logger.info(f"[Watcher] 启动 watchdog 模式，监控目录: {wiki_dir}")

        loop = asyncio.get_event_loop()
        queue = asyncio.Queue()

        event_handler = WatchdogHandler(queue)
        observer = Observer()
        observer.schedule(event_handler, str(wiki_dir), recursive=True)
        observer.start()

        await change_queue.put({
            "type": "initial_snapshot",
            "timestamp": 0,
            "mode": "watchdog"
        })
        watcher_initialized = True

        try:
            while True:
                try:
                    event = await asyncio.wait_for(queue.get(), timeout=1)
                    await change_queue.put(event)
                except asyncio.TimeoutError:
                    pass
        except Exception as e:
            logger.error(f"[Watcher] watchdog 异常: {e}")
        finally:
            observer.stop()
            observer.join()
else:
    async def watchdog_watcher():
        """Watchdog 不可用时的降级函数"""
        logger.warning("[Watcher] watchdog 不可用，使用轮询模式")
        await polling_watcher()


async def polling_watcher():
    """轮询 Watcher - 自动降级方案"""
    global last_wiki_mtime, last_backup_time, watcher_initialized

    wiki_dir = config.WIKI_DATA_DIR
    logger.info(f"[Watcher] 启动轮询模式，监控目录: {wiki_dir}")

    while True:
        await asyncio.sleep(config.WATCHER_INTERVAL)
        try:
            if not wiki_dir.exists():
                logger.warning(f"[Watcher] 目录不存在: {wiki_dir}")
                continue

            mtimes = []
            for f in wiki_dir.rglob("*.md"):
                try:
                    if f.is_file():
                        mtimes.append(f.stat().st_mtime)
                except Exception:
                    pass

            current_mtime = max(mtimes) if mtimes else 0

            if watcher_initialized and current_mtime > last_wiki_mtime:
                await change_queue.put({
                    "type": "wiki_change",
                    "timestamp": current_mtime,
                    "mtime_diff": current_mtime - last_wiki_mtime
                })
            elif not watcher_initialized:
                await change_queue.put({
                    "type": "initial_snapshot",
                    "timestamp": current_mtime,
                    "file_count": len(mtimes)
                })
                watcher_initialized = True

            last_wiki_mtime = current_mtime

            if config.WATCHER_BACKUP_INTERVAL > 0:
                current_time = asyncio.get_event_loop().time()
                if current_time - last_backup_time > config.WATCHER_BACKUP_INTERVAL:
                    await change_queue.put({"type": "backup_trigger"})
                    last_backup_time = current_time

        except Exception as e:
            logger.error(f"[Watcher] 轮询异常: {e}")


async def wiki_watcher():
    """统一的 Watcher 入口 - 自动选择模式"""
    global change_queue
    change_queue = asyncio.Queue(maxsize=100)

    if WATCHDOG_AVAILABLE:
        logger.info("[Watcher] 优先使用 watchdog 模式")
        await watchdog_watcher()
    else:
        logger.info("[Watcher] 使用轮询模式")
        await polling_watcher()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    global change_queue

    logger.info("[APP] 启动 Wiki API 服务")

    change_queue = asyncio.Queue()

    shutdown_event = asyncio.Event()

    def signal_handler(signum, frame):
        logger.info(f"[APP] 收到信号 {signum}，开始优雅关闭")
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    watcher_task = asyncio.create_task(wiki_watcher())
    logger.info("[APP] Watcher 任务已启动")

    if config.FRONTEND_DIR.exists():
        try:
            process_manager.start_process(
                "frontend",
                ["npm", "run", "dev"],
                cwd=str(config.FRONTEND_DIR),
                env={**os.environ, "PORT": str(config.FRONTEND_PORT)}
            )
            logger.info("[APP] 前端服务已启动")
        except Exception as e:
            logger.error(f"[APP] 前端启动失败: {e}")

    logger.info(f"[APP] 后端服务启动于 http://{config.API_HOST}:{config.API_PORT}")
    logger.info(f"[APP] 日志文件: {config.LOG_FILE}")

    yield

    logger.info("[APP] 关闭 Wiki API 服务")
    shutdown_event.set()
    if not watcher_task.done():
        watcher_task.cancel()
        try:
            await asyncio.wait_for(watcher_task, timeout=2.0)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            pass
    process_manager.stop_all()


app = FastAPI(
    title="Wiki API",
    version=config.API_VERSION,
    description="Wiki知识库API服务",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routes.wiki_route import router as wiki_router
app.include_router(wiki_router, prefix="/wiki")


@app.get("/events")
async def sse_events():
    """SSE 实时推送端点"""
    async def event_stream():
        while True:
            try:
                change = await asyncio.wait_for(
                    change_queue.get(),
                    timeout=config.SSE_KEEPALIVE_INTERVAL
                )
                yield f"data: {json.dumps(change)}\n\n"
            except asyncio.TimeoutError:
                yield f"data: {json.dumps({'type': 'keepalive'})}\n\n"
            except Exception as e:
                logger.error(f"[SSE] 异常: {e}")
                break

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/")
async def root():
    return {
        "message": "Wiki API",
        "version": config.API_VERSION,
        "wiki_root": str(config.WIKI_ROOT),
        "watchdog_available": WATCHDOG_AVAILABLE
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "cache_exists": config.CACHE_FILE.exists(),
        "wiki_root_exists": config.WIKI_ROOT.exists(),
        "watchdog_available": WATCHDOG_AVAILABLE
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=config.API_HOST,
        port=config.API_PORT,
        log_level="info"
    )