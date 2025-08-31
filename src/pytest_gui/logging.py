import sys

from loguru import logger

from pytest_gui.paths import Paths

__all__ = ["logger", "setup_logger"]


def setup_logger() -> None:
    """Configure the loguru logger with file and terminal handlers."""
    Paths.log_dir().mkdir(parents=True, exist_ok=True)

    # file log format
    log_format = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "Line{line: >4} ({file}): <b>{message}</b>"
    )
    # terminal log format
    stdout_format = "    <green>{time:HH:mm:ss}</green> | <b>{message}</b>"

    # Remove default logger
    logger.remove()

    # Add new logger with new log format
    logger.add(
        Paths.log_file(),
        # level="INFO",
        level="DEBUG",
        format=log_format,
        colorize=False,
        backtrace=True,
        diagnose=True,
        enqueue=True,
        filter=lambda record: record["level"].name != "TERMINAL",
        rotation="00:00",
        retention="7",
    )

    # Register a custom log level for terminal output
    #
    # This defines a **custom log level** named "TERMINAL".
    # - `no=25`: The numeric value of this level, which determines its severity.
    #   Lower values mean less severe (more verbose), higher mean more critical.
    #   - e.g., DEBUG = 10, INFO = 20, WARNING = 30.
    #   - 25 is between INFO (20) and WARNING (30), so "TERMINAL" will show messages
    #     that are more important than INFO, but less than WARNING.
    # - `color="<blue>"`: This defines the color used in terminal output for messages of this level.
    #   You can use any color supported by loguru, e.g., <cyan>, <yellow>, <red>, etc.
    #
    # To log a message at this custom level, use:
    #     logger.log("TERMINAL", "This message is for the terminal only.")
    try:
        logger.level("TERMINAL", no=25, color="<blue>")

        # Add special logger for terminal
        logger.add(
            sys.stdout,
            level="TERMINAL",
            format=stdout_format,
            colorize=False,
            backtrace=True,
            diagnose=True,
            filter=lambda record: record["level"].name == "TERMINAL",
        )
    except Exception as e:
        logger.warning(f"Failed to set up terminal logger: {e}")

    # Uncomment the line below to clear the log file on each run
    # TODO: LOG_FILE je zastaraly
    # Path.open(LOG_FILE, "w").close()


# setup_logger()
