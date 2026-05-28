"""Wiki API 配置模块 - 集中管理所有可配置项"""
import os
import logging
from pathlib import Path
from functools import lru_cache


class Config:
    """Wiki API 配置类，支持环境变量覆盖"""

    def __init__(self):
        self._setup_logging()

    def _setup_logging(self):
        """配置日志系统"""
        log_dir = self.LOG_DIR
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(name)s] %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(self.LOG_FILE),
                logging.StreamHandler()
            ]
        )

    @property
    @lru_cache(maxsize=1)
    def WIKI_ROOT(self) -> Path:
        """Wiki 根目录"""
        return Path(os.environ.get("WIKI_ROOT", "/home/dukkha/wiki")).resolve()

    @property
    @lru_cache(maxsize=1)
    def WIKI_DATA_DIR(self) -> Path:
        """Wiki 数据目录（wiki/）"""
        return self.WIKI_ROOT / os.environ.get("WIKI_DATA_SUBDIR", "wiki")

    @property
    @lru_cache(maxsize=1)
    def RAW_DIR(self) -> Path:
        """原始文件目录"""
        return self.WIKI_ROOT / os.environ.get("RAW_SUBDIR", "raw")

    @property
    @lru_cache(maxsize=1)
    def LEARNING_PATH_DIR(self) -> Path:
        """学习路径目录"""
        return self.WIKI_ROOT / os.environ.get("LEARNING_PATH_SUBDIR", "my-learning-path")

    @property
    @lru_cache(maxsize=1)
    def LOG_DIR(self) -> Path:
        """日志目录"""
        return Path(os.environ.get("LOG_DIR", str(self.WIKI_ROOT / "logs")))

    @property
    @lru_cache(maxsize=1)
    def LOG_FILE(self) -> Path:
        """日志文件路径"""
        return self.LOG_DIR / os.environ.get("LOG_FILE", "run.log")

    @property
    @lru_cache(maxsize=1)
    def FRONTEND_DIR(self) -> Path:
        """前端目录"""
        return Path(os.environ.get("FRONTEND_DIR", str(self.WIKI_ROOT / "frontend")))

    @property
    @lru_cache(maxsize=1)
    def CACHE_FILE(self) -> Path:
        """索引缓存文件"""
        return self.WIKI_DATA_DIR / os.environ.get("CACHE_FILE", "index-cache.json")

    @property
    @lru_cache(maxsize=1)
    def SCRIPTS_DIR(self) -> Path:
        """脚本目录"""
        return self.WIKI_ROOT / os.environ.get("SCRIPTS_SUBDIR", "scripts")

    @property
    @lru_cache(maxsize=1)
    def API_VERSION(self) -> str:
        """API 版本"""
        return os.environ.get("API_VERSION", "1.0.0")

    @property
    @lru_cache(maxsize=1)
    def API_HOST(self) -> str:
        """API 监听地址"""
        return os.environ.get("API_HOST", "127.0.0.1")

    @property
    @lru_cache(maxsize=1)
    def API_PORT(self) -> int:
        """API 监听端口"""
        return int(os.environ.get("API_PORT", "8000"))

    @property
    @lru_cache(maxsize=1)
    def FRONTEND_PORT(self) -> int:
        """前端端口"""
        return int(os.environ.get("FRONTEND_PORT", "3000"))

    @property
    @lru_cache(maxsize=1)
    def WATCHER_INTERVAL(self) -> float:
        """Watcher 轮询间隔（秒）"""
        return float(os.environ.get("WATCHER_INTERVAL", "1.0"))

    @property
    @lru_cache(maxsize=1)
    def WATCHER_BACKUP_INTERVAL(self) -> int:
        """Watcher 备份间隔（秒）"""
        return int(os.environ.get("WATCHER_BACKUP_INTERVAL", "300"))

    @property
    @lru_cache(maxsize=1)
    def SEARCH_TIMEOUT(self) -> int:
        """搜索超时时间（秒）"""
        return int(os.environ.get("SEARCH_TIMEOUT", "15"))

    @property
    @lru_cache(maxsize=1)
    def FIND_TIMEOUT(self) -> int:
        """文件查找超时时间（秒）"""
        return int(os.environ.get("FIND_TIMEOUT", "10"))

    @property
    @lru_cache(maxsize=1)
    def REFRESH_TIMEOUT(self) -> int:
        """刷新缓存超时时间（秒）"""
        return int(os.environ.get("REFRESH_TIMEOUT", "60"))

    @property
    @lru_cache(maxsize=1)
    def SSE_KEEPALIVE_INTERVAL(self) -> int:
        """SSE 保持连接间隔（秒）"""
        return int(os.environ.get("SSE_KEEPALIVE_INTERVAL", "30"))

    @property
    @lru_cache(maxsize=1)
    def MAX_SEARCH_RESULTS(self) -> int:
        """最大搜索结果数"""
        return int(os.environ.get("MAX_SEARCH_RESULTS", "20"))

    @property
    @lru_cache(maxsize=1)
    def MAX_PAGES_LIMIT(self) -> int:
        """最大页面列表数"""
        return int(os.environ.get("MAX_PAGES_LIMIT", "200"))

    @property
    @lru_cache(maxsize=1)
    def CONTENT_CACHE_SIZE(self) -> int:
        """内容缓存大小"""
        return int(os.environ.get("CONTENT_CACHE_SIZE", "50"))

    @property
    @lru_cache(maxsize=1)
    def WIKILINK_CACHE_SIZE(self) -> int:
        """Wikilink 转换缓存大小"""
        return int(os.environ.get("WIKILINK_CACHE_SIZE", "500"))

    @property
    @lru_cache(maxsize=1)
    def EXCLUDED_DIRS(self) -> list:
        """排除的目录列表"""
        return os.environ.get(
            "EXCLUDED_DIRS",
            ".obsidian,node_modules,.git,.rtk"
        ).split(",")

    @property
    @lru_cache(maxsize=1)
    def BACKUP_DIR(self) -> Path:
        """备份目录"""
        return self.WIKI_ROOT / os.environ.get("BACKUP_SUBDIR", ".gc_backups")

    def get_logger(self, name: str) -> logging.Logger:
        """获取指定名称的日志记录器"""
        return logging.getLogger(name)


config = Config()