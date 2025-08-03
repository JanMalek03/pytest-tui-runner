from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Checkbox, Label

from logs.logger_config import logger
from src.ui.tui.handlers.special_test_group import SpecialTestGroup

MAX_ROW_LENGTH = 3


def compose_widgets(widgets: dict) -> list:
    """Compose a list of widget layouts from a dictionary of categories and subcategories.

    Parameters
    ----------
    widgets : dict
        Dictionary containing categories as keys and subcategory dictionaries as values.

    Returns
    -------
    list
        List of composed widget layouts for each category.

    """
    layout: list = []

    for category_name, subcat in widgets.items():
        layout.append(compose_category(category_name, subcat))

    return layout


def compose_category(category_name: str, subcat: dict) -> Vertical:
    """Compose a Vertical layout for a category, including its subcategories.

    Parameters
    ----------
    category_name : str
        Name of the category.
    subcat : dict
        Dictionary containing subcategory names as keys and their associated tests as values.

    Returns
    -------
    Vertical
        A Vertical widget containing the category label and its subcategories.

    """
    category: list[Widget] = [Label(category_name, classes="category_label")]

    for subcat_name, tests in subcat.items():
        category.append(compose_subcategory(subcat_name, tests))

    return Vertical(*category, classes="category")


def compose_subcategory(subcat_name: str, tests: dict) -> Vertical:
    """Compose a Vertical layout for a subcategory, organizing its tests into rows.

    Parameters
    ----------
    subcat_name : str
        Name of the subcategory.
    tests : dict
        Dictionary containing test names as keys and lists of associated widgets as values.

    Returns
    -------
    Vertical
        A Vertical widget containing the subcategory label and its tests arranged in rows.

    """
    subcat: list[Widget] = [Label(subcat_name, classes="subcategory_label")]
    row_items: list = []

    for test_name, widget_list in tests.items():
        content: Vertical = compose_subcategory_content(test_name, widget_list)
        if len(widget_list) == 1:
            row_items.append(content)
        else:
            subcat.append(content)

    for i in range(0, len(row_items), MAX_ROW_LENGTH):
        row: list = row_items[i : i + MAX_ROW_LENGTH]
        subcat.append(Horizontal(*row, classes="subcategory_row"))

    return Vertical(*subcat, classes="subcategory")


def compose_subcategory_content(test_name: str, widget_list: list[Widget]) -> Vertical:
    """Compose the content for a subcategory test, returning a Vertical layout.

    Parameters
    ----------
    test_name : str
        Name of the test.
    widget_list : list[Widget]
        List of widgets associated with the test.

    Returns
    -------
    Vertical
        A Vertical widget containing the test's content.

    Raises
    ------
    ValueError
        If no widgets are found for the test.
    """
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


def is_basic_test(widget_list: list[Widget]) -> bool:
    """Check if the widget list contains only a single Checkbox."""
    return len(widget_list) == 1 and isinstance(widget_list[0], Checkbox)
