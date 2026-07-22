"""
logger_setup.py — shared logging config for the classnote MCP examples.

Import get_logger(__name__) instead of sprinkling print() everywhere:
    - console shows INFO and up (readable while you watch a run happen)
    - logs/mcp_client.log keeps DEBUG and up (full detail, kept for later)
    - the file rotates so repeated runs don't grow it forever
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).parent / "logs"
LOG_FILE = LOG_DIR / "mcp_client.log"

_configured = False


def get_logger(name: str = "mcp_client") -> logging.Logger:
    global _configured

    if not _configured:
        LOG_DIR.mkdir(exist_ok=True)

        formatter = logging.Formatter(
            fmt="%(asctime)s  %(levelname)-7s  %(name)s  %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        root.addHandler(console_handler)
        root.addHandler(file_handler)

        _configured = True

    return logging.getLogger(name)
