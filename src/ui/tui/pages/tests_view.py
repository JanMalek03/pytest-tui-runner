from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Checkbox, Input, Select, Button
from src.config.config_loader import ConfigLoader
from src.ui.tui.handlers.button_handler import ButtonHandler


class TestsView(Vertical):
    def __init__(self):
        super().__init__()
        self.config = ConfigLoader.load_config("src/config/default.yaml")
        self.widgets = {}
        self.generate_widgets()

    async def on_mount(self) -> None:
        terminal_view = self.app.terminal_view
        self.button_handler = ButtonHandler(self.widgets, terminal_view)

    def generate_widgets(self):
        for category in self.config["categories"]:
            category_name = category["name"]
            self.widgets[category_name] = {}

            for subcategory in category.get("subcategories", []):
                subcategory_name = subcategory["name"]
                self.widgets[category_name][subcategory_name] = {}

                for test in subcategory["tests"]:
                    widget = None
                    if test["widget"] == "checkbox":
                        widget = Checkbox(test["name"])
                    elif test["widget"] == "text_input":
                        widget = Input(placeholder=test["parameters"].get("placeholder", ""))
                    elif test["widget"] == "dropdown":
                        options = test["parameters"].get("options", [])
                        widget = Select([(opt, opt) for opt in options])

                    if widget:
                        self.widgets[category_name][subcategory_name][test["name"]] = widget

    def compose(self):
        for category_name, subcategories in self.widgets.items():
            yield Label(category_name)
            category_content = []
            for subcategory_name, widgets in subcategories.items():
                category_content.append(Vertical(Label(subcategory_name), *widgets.values()))
            category_container = Horizontal(*category_content)
            yield category_container

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
                self.app.exit()
