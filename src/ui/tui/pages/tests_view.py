from collections.abc import Iterator
from typing import TYPE_CHECKING

from textual.containers import Horizontal, ScrollableContainer, Vertical
from textual.widget import Widget
from textual.widgets import Button

from logs.logger_config import logger
from src.config.paths import CONFIG_PATH
from src.ui.tui.handlers.button_handler import ButtonHandler

if TYPE_CHECKING:
    from src.ui.tui.pages.terminal_view import TerminalView
    from src.utils.types.config import TestConfig
from src.config.config_loader import load_config
from src.utils.widgets.manager import WidgetManager


class TestsView(Vertical):
    """A page for displaying and managing tests widgets in the TUI.

    Handles loading configuration, managing widgets, and responding to button events.
    """

    def __init__(self) -> None:
        """Initialize the TestsView, loading configuration and setting up the widget manager."""
        super().__init__()
        self.config: TestConfig = load_config(CONFIG_PATH)
        self.widget_manager = WidgetManager(self.config)

    async def on_mount(self) -> None:
        """Set up the button handler when the view is mounted."""
        terminal_view: TerminalView = self.app.terminal_view
        self.button_handler = ButtonHandler(self.widget_manager.widgets, terminal_view)

    def compose(self) -> Iterator[Widget]:
        """Compose the widgets for the tests view, including the scrollable test widgets and control buttons.

        Yields
        ------
        Widget
            The scrollable container of test widgets and the horizontal container of control buttons.

        """
        yield ScrollableContainer(*self.widget_manager.compose())

        self.widget_manager.load_state()

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
                logger.info("Add button pressed")
            case "exit":
                self.widget_manager.save_state()
                self.app.exit()
