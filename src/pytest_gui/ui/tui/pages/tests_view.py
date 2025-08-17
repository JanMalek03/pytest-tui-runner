from collections.abc import Iterator
from typing import TYPE_CHECKING

from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.widget import Widget
from textual.widgets import Button

from logs.logger_config import logger
from src.pytest_gui.config.paths import CONFIG_PATH
from src.pytest_gui.ui.tui.handlers.button_handler import ButtonHandler

if TYPE_CHECKING:
    from src.pytest_gui.ui.tui.pages.terminal_view import TerminalView
    from src.pytest_gui.utils.types.config import TestConfig

from src.pytest_gui.config.config_loader import load_config
from src.pytest_gui.utils.widgets.manager import WidgetManager


class TestsView(Vertical):
    """A page for displaying and managing tests widgets in the TUI.

    Handles loading configuration, managing widgets, and responding to button events.
    """

    def __init__(self) -> None:
        """Initialize the TestsView, loading configuration and setting up the widget manager."""
        super().__init__()

        # Load a user-defined test configuration.
        # Categories, subcategories, tests and their arguments are defined here
        self.config: TestConfig = load_config(CONFIG_PATH)

        # Create a WidgetManager class that is responsible for all work with widgets.
        # It will create widgets according to the config and then load their stored values
        self.widget_manager = WidgetManager(self.config)

    async def on_mount(self) -> None:
        """Set up the button handler when the view is mounted."""
        # Gets a handler for the terminal page, which is stored in the main application.
        # Thanks to this, we will be able to display the progress of the tests in the terminal
        terminal_view: TerminalView = self.app.terminal_view

        # ButtonHandler handles all actions associated with pressing buttons
        self.button_handler = ButtonHandler(self.widget_manager.widgets, terminal_view)

    def compose(self) -> Iterator[Widget]:
        """Compose the widgets for the tests view, including the scrollable test widgets and control buttons.

        Yields
        ------
        Widget
            The scrollable container of test widgets and the horizontal container of control buttons.

        """
        # A container that contains all widgets associated with tests
        yield ScrollableContainer(*self.widget_manager.compose())

        # A container that contains all the additional buttons for controlling the test
        yield Horizontal(
            Button("Run tests", id="run_tests", classes="button"),
            Button("Check all", id="check_all", classes="button"),
            Button("Uncheck all", id="uncheck_all", classes="button"),
            Button("Exit", id="exit", classes="button"),
            id="button_container",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events and trigger corresponding actions.

        Parameters
        ----------
        event : Button.Pressed
            The button press event containing the button ID.

        """
        match event.button.id:
            case "run_tests":
                self.button_handler.run_tests()
            case "check_all":
                self.button_handler.check_all()
            case "uncheck_all":
                self.button_handler.uncheck_all()
            case "add_button":
                # TODO: presunout logger fo button_handler.add()
                logger.info("Add button pressed")
            case "exit":
                self.widget_manager.save_state()
                self.app.exit()
