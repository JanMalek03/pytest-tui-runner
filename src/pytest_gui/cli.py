import subprocess
import sys

import click

from pytest_gui.logs.logger_config import logger


@click.group()
def cli() -> None:
    """CLI for pytest-gui plugin."""


@cli.command()
def run() -> None:
    """Run the terminal application."""
    try:
        logger.info("Starting the application...")
        subprocess.run(["uv", "run", "-m", "src.pytest_gui.ui.tui.app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error launching the application: {e}")
        logger.error(f"Error launching the application: {e}")
        sys.exit(1)
