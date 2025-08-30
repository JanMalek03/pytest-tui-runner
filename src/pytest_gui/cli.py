import subprocess
import sys
from pathlib import Path

import click

from pytest_gui.logging import logger, setup_logger
from pytest_gui.paths import Paths, find_project_root_by_tests
from pytest_gui.ui.tui.app import TestRunnerApp


@click.group()
def cli() -> None:
    """CLI for pytest-gui plugin."""


@cli.command()
@click.argument("project_path", required=False, type=click.Path(exists=True, file_okay=False))
def run(project_path: str | None) -> None:
    """Run the terminal application."""
    try:
        if project_path:
            root = Path(project_path).resolve()
            Paths.set_user_root(root)
        else:
            root = find_project_root_by_tests(Path.cwd())
            if root is None:
                logger.error("Could not find project root (missing 'tests' directory).")
                sys.exit(1)
            Paths.set_user_root(root)

        setup_logger()
        logger.info(f"Using project root: {root}")

        logger.info("Starting the application...")

        # subprocess.run(["uv", "run", "-m", "pytest_gui.ui.tui.app"], check=True)

        app = TestRunnerApp()
        app.run()

    except subprocess.CalledProcessError as e:
        print(f"Error launching the application: {e}")
        logger.error(f"Error launching the application: {e}")
        sys.exit(1)
