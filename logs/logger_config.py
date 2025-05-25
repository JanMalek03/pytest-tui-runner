import sys
from pathlib import Path

from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# LOG_FILE = LOG_DIR / "app-{time:YYYY-MM-DD}.log"
LOG_FILE = LOG_DIR / "app.log"

LOG_FORMAT = "<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | Line{line: >4} ({file}): <b>{message}</b>"
STDOUT_FORMAT = "    <green>{time:HH:mm:ss}</green> | <b>{message}</b>"

logger.level("TERMINAL", no=25, color="<blue>", icon="🔧")

# Remove default logger
logger.remove()

# Add new logger
logger.add(
    LOG_FILE,
    # level="INFO",
    level="DEBUG",
    format=LOG_FORMAT,
    colorize=False,
    backtrace=True,
    diagnose=True,
    enqueue=True,
    filter=lambda record: record["level"].name != "TERMINAL",
    rotation="00:00",
    retention=7,
)

# Add special logger for terminal
logger.add(
    sys.stdout,
    level="TERMINAL",
    format=STDOUT_FORMAT,
    colorize=False,
    backtrace=True,
    diagnose=True,
    filter=lambda record: record["level"].name == "TERMINAL",
)

# Uncomment the line below to clear the log file on each run
# Path.open("logs/app.log", "w").close()

__all__ = ["logger"]