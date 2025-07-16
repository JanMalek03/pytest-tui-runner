from textual.containers import Vertical, Horizontal, ScrollableContainer, VerticalScroll
from textual.widgets import Label, Button
from textual.scroll_view import ScrollView
from src.config.config_loader import ConfigLoader
from src.ui.tui.handlers.button_handler import ButtonHandler
from src.utils.widgets.manager import WidgetManager
from logs.logger_config import logger
from src.config.paths import CONFIG_PATH
import yaml


class TestsView(Vertical):
    def __init__(self):
        super().__init__()
        assert CONFIG_PATH.exists(), f"Configuration file {CONFIG_PATH} does not exist."
        with open(CONFIG_PATH, "r", encoding="utf-8") as file:
            self.config = yaml.safe_load(file)

        self.widgetManager = WidgetManager(self.config)

    async def on_mount(self) -> None:
        terminal_view = self.app.terminal_view
        self.button_handler = ButtonHandler(self.widgetManager.widgets, terminal_view)

    def compose(self):
        yield ScrollableContainer(*self.widgetManager.compose())

        self.widgetManager.load_state()

        yield Horizontal(
            Button("Run tests", id="run_tests", classes="button"),
            Button("Check all", id="check_all", classes="button"),
            Button("Uncheck all", id="uncheck_all", classes="button"),
            Button("Exit", id="exit", classes="button"),
            id="button_container",
        )

    def on_button_pressed(self, event):
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
                self.widgetManager.save_state()
                self.app.exit()
