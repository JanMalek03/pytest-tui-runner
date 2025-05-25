import subprocess
import sys
from logs.logger_config import logger

def main():
    try:
        logger.info("Starting the application...")
        subprocess.run(["uv", "run", "-m", "src.ui.tui.app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching the application: {e}")
        logger.error(f"Error launching the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
