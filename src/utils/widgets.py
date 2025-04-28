from typing import Iterator
from textual.widgets import Checkbox, Input, Select, Label
from textual.containers import Vertical, Horizontal
from logs.logger_config import logger

def generate_widgets(config):
    widgets = {}

    for category in config["categories"]:
        category_name = category["name"]
        widgets[category_name] = {}

        for subcategory in category.get("subcategories", []):
            subcategory_name = subcategory["name"]
            widgets[category_name][subcategory_name] = _generate_subcategory_widgets(subcategory)

    return widgets


def _generate_subcategory_widgets(subcategory):
    widgets = {}

    for test in subcategory.get("tests", []):
        test_name = test["name"]
        widgets[test_name] = _get_test_widget(test)

    return widgets


def _get_test_widget(test):
    widgets = None

    if test.get("type") == "normal":
        widgets = _get_widget_for_normal_test(test)

    elif test.get("type") == "special":
        widgets = _get_widget_for_special_test(test)

    return widgets


def _get_widget_for_normal_test(test):
    return [Checkbox(test["name"])]


def _get_widget_for_special_test(test):
    widgets = []
    arguments = test["arguments"]

    for arg in arguments:
        if arg["arg_type"] == "select":
            options = arg.get("options")
            widgets.append(Select([(opt, opt) for opt in options]))
        elif arg["arg_type"] == "text_input":
            widgets.append(Input(placeholder=arg.get("placeholder")))

    return widgets


def compose_widgets(widgets: dict[str, dict[str, dict[str, list]]]) -> Iterator[Horizontal]:
    for category_name, subcategories in widgets.items():
        yield Label(category_name)
        category_content = []

        for subcategory_name, tests in subcategories.items():
            normal_test_widgets = []
            special_test_layouts = []

            for test_name, widget_list in tests.items():
                if len(widget_list) == 1 and isinstance(widget_list[0], Checkbox):
                    normal_test_widgets.append(widget_list[0])
                else:
                    special_test_layout = Vertical(Label(test_name), *widget_list)
                    special_test_layouts.append(special_test_layout)

            if normal_test_widgets:
                category_content.append(Vertical(Label(subcategory_name), *normal_test_widgets))

            category_content.extend(special_test_layouts)
        
        if category_content:
            yield Horizontal(*category_content)
