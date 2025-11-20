import subprocess
import sys
from pathlib import Path

import click

from pytest_tui_runner.logging import logger, setup_logger
from pytest_tui_runner.paths import Paths, find_project_root_by_folder
from pytest_tui_runner.ui.tui.app import TestRunnerApp


@click.group()
def cli() -> None:
    """CLI for pytest-tui-runner plugin."""


@cli.command()
@click.argument("project_path", required=False, type=click.Path(exists=True, file_okay=False))
@click.option(
    "--init",
    "-i",
    is_flag=True,
    default=False,
    help="Creates a library folder and config file in the current directory.",
)
def run(project_path: str | None, init: bool) -> None:
    """Run the terminal application."""
    try:
        if project_path:
            root: Path = Path(project_path).resolve()
            Paths.set_user_root(root)
            if init:
                setup_project(root)
        elif init:
            root = Path.cwd().resolve()
            setup_project(root)
        else:
            root = find_project_root_by_folder(Path.cwd(), [Paths.APP_FOLDER])
            if root is None:
                logger.error(
                    """Could not find project root.
    You can run the application with the --init option, which will create in the current folder all the necessary things to run the application (the .pytest_tui_runner folder and the config.yaml file).
    !!! However, you must be in the root directory of your project with tests, otherwise this initialization will be done in the wrong place.""",
                )
                sys.exit(1)
            Paths.set_user_root(root)

        setup_logger()
        logger.info("=============================== NEW RECORD ===============================")
        logger.debug("---------------------- APPLICATION PREPARATION ----------------------")
        logger.info(f"Path to user's project found: '{root}'")

        logger.info("▶️ Starting the application...")
        app = TestRunnerApp()
        app.run()

    except subprocess.CalledProcessError as e:
        logger.error(f"Error launching the application: {e}")
        sys.exit(1)


def setup_project(user_root: Path) -> None:
    """Set up a default .pytest_tui_runner folder and config file in the current directory."""
    Paths.set_user_root(user_root)

    target_dir = Paths.app_dir()
    config_file = Paths.config()

    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        click.echo(f"✅ Folder created: {target_dir}")
    else:
        click.echo(f"ℹ️ Folder '{target_dir}' already exists.")

    if not config_file.exists():
        config_file.write_text(
            """categories:
  - label: "Your category label"
    subcategories:
      - label: "Your subcategory label"
        tests:
          - label: "Your test label"
            test_name: "your_test_name"
""",
        )
        click.echo(f"✅ Created config file with some example data: {config_file}")
    else:
        click.echo(f"ℹ️ File '{config_file}' already exists.")
