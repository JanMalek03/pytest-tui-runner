from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Checkbox, Label

from logs.logger_config import logger
from src.pytest_gui.ui.tui.handlers.special_test_group import SpecialTestGroup
from src.pytest_gui.utils.types.widgets import (
    CategoryDict,
    SubCategoryDict,
    TestWidgets,
    WidgetsDict,
)

MAX_ROW_LENGTH = 3


def compose_widgets(widgets: WidgetsDict) -> list[Vertical]:
    """Compose a list of widget layouts from a dictionary of categories and subcategories."""
    layout: list[Vertical] = []

    for category_name, category in widgets.items():
        layout.append(compose_category(category_name, category))

    return layout


def compose_category(category_name: str, category: CategoryDict) -> Vertical:
    """Compose a Container layout for a category, including its subcategories."""
    items: list[Widget] = [Label(category_name, classes="category_label")]

    for subcategory_name, subcategory in category.items():
        items.append(compose_subcategory(subcategory_name, subcategory))

    return Vertical(*items, classes="category")


def compose_subcategory(subcategory_name: str, subcategory: SubCategoryDict) -> Vertical:
    """Compose a Container layout for a subcategory, organizing its tests into rows.

    Normal checkbox tests put in rows, according to MAX_ROW_LENGTH.
    """
    items: list[Widget] = [Label(subcategory_name, classes="subcategory_label")]
    row_buffer: list[Widget] = []

    for test_name, widget_list in subcategory.items():
        test_layout: Vertical = compose_test(test_name, widget_list)

        if is_basic_test(widget_list):
            row_buffer.append(test_layout)
            flush_row(row_buffer, items, require_full=True)
        else:
            flush_row(row_buffer, items)
            items.append(test_layout)

    flush_row(row_buffer, items)
    return Vertical(*items, classes="subcategory")


def compose_test(test_name: str, widget_list: TestWidgets) -> Vertical:
    """Return the test container.

    The test will be either an ordinary checkbox or a widget of the
    SpecialTestGroup type (for tests with arguments).
    """
    if not widget_list:
        logger.error(f"No widgets found for test {test_name}.")
        raise ValueError(f"No widgets found for test {test_name}.")

    # Basic test
    if is_basic_test(widget_list):
        return Vertical(widget_list[0], classes="subcategory_content")

    # Test with arguments
    return Vertical(
        Label(test_name, classes="subcategory_label"),
        SpecialTestGroup(widget_list),
        classes="subcategory_content",
    )


def is_basic_test(widget_list: TestWidgets) -> bool:
    """Check if the widget list contains only a single Checkbox."""
    return len(widget_list) == 1 and isinstance(widget_list[0], Checkbox)


def flush_row(row_buffer: list[Widget], items: list[Widget], *, require_full: bool = False) -> None:
    """Flush the row buffer into items.

    If require_full is True, flush only if buffer reached MAX_ROW_LENGTH.
    """
    if not row_buffer:
        return

    if require_full and len(row_buffer) < MAX_ROW_LENGTH:
        return

    items.append(Horizontal(*row_buffer, classes="subcategory_row"))
    row_buffer.clear()
