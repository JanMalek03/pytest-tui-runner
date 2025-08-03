import asyncio

from logs.logger_config import logger
from src.config.paths import PYTEST_INI_PATH, TEST_PATH
from src.ui.tui.pages.terminal_view import TerminalView
from src.utils.pytest.arguments import build_pytest_arguments


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

    def __init__(self, widgets: dict, terminal_view: TerminalView) -> None:
        """Initialize ButtonHandler with widgets and terminal view.

        Parameters
        ----------
        widgets : dict
            Dictionary of widgets representing test options.
        terminal_view
            The terminal view interface for displaying output.

        """
        self.widgets = widgets
        self.terminal_view = terminal_view
        self._background_tasks = set()

    def run_tests(self) -> None:
        """Initiate running tests asynchronously.

        This method schedules the asynchronous test runner to execute in the event loop.
        """
        asyncio.create_task(self._run_tests_async())

    async def _run_tests_async(self) -> None:
        logger.info(f"Testing: {TEST_PATH}")

        if not TEST_PATH.exists():
            logger.error(f"Test path {TEST_PATH} does not exist.")
            return

        args = build_pytest_arguments(self.widgets, PYTEST_INI_PATH)

        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            cwd=TEST_PATH,
        )

        logger.info(f"Running tests in {TEST_PATH}")
        self.terminal_view.write_line("Running tests...\n")

        if process.stdout is None:
            raise RuntimeError("Process stdout is not available.")
        async for line in process.stdout:
            decoded = line.decode().rstrip()
            self.terminal_view.write_line(decoded)

        await process.wait()
        self.terminal_view.write_line("\nTests finished.")

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
