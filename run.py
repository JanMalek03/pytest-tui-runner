import subprocess
import sys

from pytest_tui_runner.logging import logger


def main() -> None:
    """Run the terminal application."""
    try:
        logger.info("Starting the application...")
        subprocess.run(["uv", "run", "-m", "pytest_tui_runner.ui.tui.app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching the application: {e}")
        logger.error(f"Error launching the application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
