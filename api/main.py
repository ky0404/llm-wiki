"""API 主入口"""
import os
import sys
import subprocess
import logging
import threading
from pathlib import Path

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "run.log"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Wiki API",
    version="1.0.0",
    description="Wiki知识库API服务"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 导入路由
from routes.wiki_route import router as wiki_router
app.include_router(wiki_router, prefix="/wiki")


@app.get("/")
async def root():
    return {"message": "Wiki API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}


def start_frontend():
    """启动前端服务"""
    frontend_dir = Path(__file__).parent.parent / "frontend"
    logger.info(f"[FRONTEND] 启动前端: {frontend_dir}")
    try:
        subprocess.run(
            ["npm", "run", "dev"],
            cwd=str(frontend_dir),
            check=True
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"[FRONTEND] 启动失败: {e}")


if __name__ == "__main__":
    import uvicorn
    
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()
    logger.info("[BACKEND] 启动后端服务: http://localhost:8000")
    logger.info("[FRONTEND] 启动前端服务: http://localhost:3000")
    logger.info(f"[LOG] 日志文件: {LOG_FILE}")
    
    uvicorn.run(app, host="127.0.0.1", port=8000)
