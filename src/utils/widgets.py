import json
from typing import Iterator
from textual.widgets import Checkbox, Input, Select, Label, Button
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

    initialize_widgets(widgets)

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
            widgets.append(Select([(opt, opt) for opt in options], allow_blank=False, name=arg["name"]))
        elif arg["arg_type"] == "text_input":
            widgets.append(Input(placeholder=arg.get("placeholder"), name=arg["name"]))

    return widgets


def initialize_widgets(widgets: dict[str, dict[str, dict[str, list]]]):
    with open("widgets_state.json", "r", encoding="utf-8") as f:
        saved_values = json.load(f)

    for category, subcategories in widgets.items():
        for subcategory, tests in subcategories.items():
            for test_name, widget_list in tests.items():
                for i, widget in enumerate(widget_list):
                    if isinstance(widget, Input):
                        widget.value = saved_values[category][subcategory][test_name][i][1]
                    elif isinstance(widget, Select):
                        select_values = list(widget._legal_values)
                        # select_values = sorted(select_values, key=int)
                        widget_list[i] = Select.from_values(
                            values=select_values,
                            name=widget.name,
                            allow_blank=widget._allow_blank,
                            value=saved_values[category][subcategory][test_name][i][1],
                        )
                    elif isinstance(widget, Checkbox):
                        widget.value = saved_values[category][subcategory][test_name][i][1]


def save_widget_values(widgets: dict[str, dict[str, dict[str, list]]], filename: str):
    saved_values = {}

    for category, subcategories in widgets.items():
        saved_values[category] = {}
        for subcategory, tests in subcategories.items():
            saved_values[category][subcategory] = {}
            for test_name, widget_list in tests.items():
                saved_values[category][subcategory][test_name] = []
                for widget in widget_list:
                    saved_values[category][subcategory][test_name].append((widget.name, widget.value))

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(saved_values, f, indent=2)


def compose_widgets(widgets: dict[str, dict[str, dict[str, list]]]) -> Iterator[Horizontal]:
    for category_name, subcategories in widgets.items():
        yield Label(category_name, classes="category_label")
        category_content = []

        for subcategory_name, tests in subcategories.items():
            normal_test_widgets = []
            special_test_layouts = []

            for test_name, widget_list in tests.items():
                if len(widget_list) == 1 and isinstance(widget_list[0], Checkbox):
                    normal_test_widgets.append(widget_list[0])
                else:
                    add_button = Button("+", variant="primary", classes="add_button")

                    special_test_layout = Vertical(
                        Label(test_name, classes="subcategory_label"),
                        Horizontal(
                            add_button,
                            *widget_list,
                            classes="special_test_row"
                        ),
                    )
                    special_test_layouts.append(special_test_layout)

            if normal_test_widgets:
                category_content.append(Vertical(Label(subcategory_name, classes="subcategory_label"), *normal_test_widgets))

            category_content.extend(special_test_layouts)
        
        if category_content:
            yield Horizontal(classes="category_horizontal", *category_content)
