import asyncio
from asyncio.subprocess import Process
from pathlib import Path

from pytest_gui.config.paths import PYTEST_INI_PATH, TEST_PATH
from pytest_gui.logs.logger_config import logger
from pytest_gui.ui.tui.pages.terminal_view import TerminalView
from pytest_gui.utils.pytest.arguments import build_pytest_arguments
from pytest_gui.utils.types.widgets import WidgetsDict


class ButtonHandler:
    """Handles button actions in the TUI, such as running tests and managing widget states.

    Attributes
    ----------
    widgets : dict
        Dictionary of widgets representing test options.
    terminal_view
        The terminal view interface for displaying output.

    Methods
    -------
    run_tests()
        Initiates running tests asynchronously.
    check_all()
        Checks all test option widgets.
    uncheck_all()
        Unchecks all test option widgets.

    """

    def __init__(self, widgets: WidgetsDict, terminal_view: TerminalView) -> None:
        """Initialize ButtonHandler with widgets and terminal view.

        Parameters
        ----------
        widgets : dict
            Dictionary of widgets representing test options.
        terminal_view
            The terminal view interface for displaying output.

        """
        self.widgets: WidgetsDict = widgets
        self.terminal_view: TerminalView = terminal_view

    def run_tests(self) -> None:
        """Initiate running tests asynchronously.

        This method schedules the asynchronous test runner to execute in the event loop.
        """
        asyncio.create_task(self._run_tests_async())

    async def _run_tests_async(self) -> None:
        if not self._validate_test_path(TEST_PATH):
            return

        args: list[str] = self._build_test_command()

        await self._execute_test_process(args, cwd=TEST_PATH)

    def _validate_test_path(self, path: Path) -> bool:
        """Check if test path exists."""
        if not path.exists():
            logger.error(f"Test path {path} does not exist.")
            self.terminal_view.write_line(f"Error: Test path {path} not found.\n")
            return False
        return True

    def _build_test_command(self) -> list[str]:
        """Build the pytest command arguments."""
        return build_pytest_arguments(self.widgets, PYTEST_INI_PATH)

    async def _execute_test_process(self, args: list[str], cwd: Path) -> None:
        """Run a subprocess for tests and stream output to terminal."""
        logger.info(f"Running tests in {cwd}")
        self.terminal_view.write_line("Running tests...\n")

        process: Process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            cwd=cwd,
        )

        if not process.stdout:
            raise RuntimeError("Process stdout is not available.")

        await self._stream_process_output(process)
        await process.wait()
        self.terminal_view.write_line("\nTests finished.")

    async def _stream_process_output(self, process: Process) -> None:
        """Stream process stdout to terminal line by line."""
        assert process.stdout is not None
        async for line in process.stdout:
            self.terminal_view.write_line(line.decode().rstrip())

    def check_all(self) -> None:
        """Check all test option widgets.

        Sets the value of all boolean widgets in the test options to True.
        """
        # for category in self.widgets.values():
        #     for subcategory in category.values():
        #         for widget in subcategory.values():
        #             if hasattr(widget, "value") and isinstance(widget.value, bool):
        #                 widget.value = True

    def uncheck_all(self) -> None:
        """Uncheck all test option widgets.

        Sets the value of all boolean widgets in the test options to False.
        """
        # for category in self.widgets.values():
        #     for subcategory in category.values():
        #         for widget in subcategory.values():
        #             if hasattr(widget, "value") and isinstance(widget.value, bool):
        #                 widget.value = False

    def _build_pytest_args(self) -> None:
        pass
        # args = []
        # for category, subcategories in self.widgets.items():
        #     for subcategory, widgets in subcategories.items():
        #         for test_name, widget in widgets.items():
        #             if isinstance(widget.value, bool) and widget.value:
        #                 flag = self._name_to_flag(test_name)
        #                 if flag:
        #                     args.append(flag)
        #             elif hasattr(widget, "value") and isinstance(widget.value, str):
        #                 if widget.value:
        #                     args.append(f"--{test_name}={widget.value}")
        # return args

    def _name_to_flag(self, name: str) -> str:
        pass
        # return f"--run-{name.replace(' ', '_').lower()}"
