from textual.containers import Vertical, Horizontal
from textual.widgets import Label, Checkbox, Input, Select, Button
from src.config.config_loader import ConfigLoader


class TestsView(Vertical):
    def __init__(self):
        super().__init__()
        self.config = ConfigLoader.load_config("src/config/default.yaml")
        self.widgets = {}
        self.generate_widgets()

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
            Button("Spustit testy", id="run_tests", classes="button"),
            Button("Zaškrtnout vše", id="check_all", classes="button"),
            Button("Odškrtnout vše", id="uncheck_all", classes="button"),
            classes="button-container"
        )
