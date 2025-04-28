from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Button
from src.config.config_loader import ConfigLoader
from src.ui.tui.handlers.button_handler import ButtonHandler
from src.utils.widgets import generate_widgets, compose_widgets, save_widget_values
from logs.logger_config import logger


class TestsView(Vertical):
    def __init__(self):
        super().__init__()
        self.config = ConfigLoader.load_config("src/config/default.yaml")
        self.widgets = generate_widgets(self.config)
        logger.debug(f"Generated tests: {self.widgets}")


    async def on_mount(self) -> None:
        terminal_view = self.app.terminal_view
        self.button_handler = ButtonHandler(self.widgets, terminal_view)

    def compose(self):
        yield from compose_widgets(self.widgets)

        yield Horizontal(
            Button("Run tests", id="run_tests", classes="button"),
            Button("Check all", id="check_all", classes="button"),
            Button("Uncheck all", id="uncheck_all", classes="button"),
            Button("Exit", id="exit", classes="button"),
            classes="button-container"
        )

    def on_button_pressed(self, event):
        match event.button.id:
            case "run_tests":
                self.button_handler.run_tests()
            case "check_all":
                self.button_handler.check_all()
            case "uncheck_all":
                self.button_handler.uncheck_all()
            case "exit":
                save_widget_values(self.widgets, "widgets_state.json")
                self.app.exit()
