from typing import Iterator
from textual.widgets import Checkbox, Label
from textual.containers import Vertical, Horizontal, Grid
from src.ui.tui.handlers.special_test_group import SpecialTestGroup
from logs.logger_config import logger
import json

MAX_ROW_LENGTH = 3

def compose_widgets(widgets):
    layout = []

    for category_name, subcat in widgets.items():
        layout.append(compose_category(category_name, subcat))

    return layout


def compose_category(category_name, subcat):
    category = [Label(category_name, classes="category_label")]

    for subcat_name, tests in subcat.items():
        category.append(compose_subcategory(subcat_name, tests))

    return Vertical(*category, classes="category")


def compose_subcategory(subcat_name, tests):
    subcat = [Label(subcat_name, classes="subcategory_label")]
    row_items = []

    for test_name, widget_list in tests.items():
        content = compose_subcategory_content(test_name, widget_list)
        if len(widget_list) == 1:
            row_items.append(content)
        else:
            subcat.append(content)

    for i in range(0, len(row_items), MAX_ROW_LENGTH):
        row = row_items[i:i + MAX_ROW_LENGTH]
        subcat.append(Horizontal(*row, classes="subcategory_row"))

    return Vertical(*subcat, classes="subcategory")


def compose_subcategory_content(test_name, widget_list):
    if not widget_list:
            logger.error(f"No widgets found for test {test_name}.")
            raise ValueError(f"No widgets found for test {test_name}.")

    subcat_content = []

    if is_basic_test(widget_list):
        subcat_content.append(widget_list[0])
    else:
        group = SpecialTestGroup(widget_list)
        subcat_content.append(Label(test_name, classes="subcategory_label"))
        subcat_content.append(group)

    return Vertical(*subcat_content, classes="subcategory_content")


def is_basic_test(widget_list):
    """Check if the widget list contains only a single Checkbox."""
    return len(widget_list) == 1 and isinstance(widget_list[0], Checkbox)
