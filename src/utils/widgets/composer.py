from typing import Iterator
from textual.widgets import Checkbox, Label
from textual.containers import Vertical, Horizontal, Grid
from src.ui.tui.handlers.special_test_group import SpecialTestGroup
from logs.logger_config import logger

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
    max_row_length = 3

    row = []
    for test_name, widget_list in tests.items():
        if len(widget_list) == 1:
            row.append(compose_subcategory_content(test_name, widget_list))
            if len(row) == max_row_length:
                subcat.append(Horizontal(*row, classes="subcategory_row"))
                row = []
        else:
            subcat.append(compose_subcategory_content(test_name, widget_list))

    if row:
        subcat.append(Horizontal(*row, classes="subcategory_row"))

    logger.debug(subcat_name)
    logger.debug(subcat)
    return Vertical(*subcat, classes="subcategory")


def compose_subcategory_content(test_name, widget_list):
    subcat_content = []

    if len(widget_list) == 1 and isinstance(widget_list[0], Checkbox):
        subcat_content.append(widget_list[0])
    else:
        group = SpecialTestGroup(test_name, widget_list)
        subcat_content.append(Label(test_name, classes="subcategory_label"))
        subcat_content.append(group)

    return Vertical(*subcat_content, classes="subcategory_content")
