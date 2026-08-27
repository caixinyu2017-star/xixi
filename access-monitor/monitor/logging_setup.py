"""日志：终端一份（带颜色标记的简洁格式）+ 文件一份（按天滚动，保留 14 天）。"""
from __future__ import annotations

import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class _ConsoleFormatter(logging.Formatter):
    ICONS = {"DEBUG": "·", "INFO": "•", "WARNING": "!", "ERROR": "✗", "CRITICAL": "✗"}

    def format(self, record: logging.LogRecord) -> str:
        icon = self.ICONS.get(record.levelname, "•")
        return f"{self.formatTime(record, '%H:%M:%S')} {icon} {record.getMessage()}"


def setup_logging(log_dir: Path, level: str = "INFO", quiet: bool = False) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    for handler in list(root.handlers):
        root.removeHandler(handler)

    console = logging.StreamHandler(sys.stderr)
    console.setLevel(getattr(logging, level.upper(), logging.INFO) if not quiet else logging.WARNING)
    console.setFormatter(_ConsoleFormatter())
    root.addHandler(console)

    file_handler = TimedRotatingFileHandler(
        log_dir / "monitor.log", when="midnight", backupCount=14, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)-7s %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S"
    ))
    root.addHandler(file_handler)

    # 第三方库太吵
    for noisy in ("urllib3", "requests", "PIL"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
    # asyncio 在 Playwright 关闭时会喷 "Task was destroyed but it is pending"，
    # 无害但很吓人，会盖住真正要看的信息
    logging.getLogger("asyncio").setLevel(logging.CRITICAL)
