from typing import Iterator
from textual.widgets import Checkbox, Label
from textual.containers import Vertical, Horizontal
from src.ui.tui.handlers.special_test_group import SpecialTestGroup

def compose_widgets(widgets) -> Iterator[Horizontal]:
    for cat_name, subcats in widgets.items():
        yield Label(cat_name, classes="category_label")
        category_content = []

        for subcat_name, tests in subcats.items():
            normal, special = [], []

            for test_name, widget_list in tests.items():
                if len(widget_list) == 1 and isinstance(widget_list[0], Checkbox):
                    normal.append(widget_list[0])
                else:
                    group = SpecialTestGroup(test_name, widget_list)
                    special.append(Vertical(Label(test_name, classes="subcategory_label"), group))

            if normal:
                category_content.append(Vertical(Label(subcat_name, classes="subcategory_label"), *normal))
            category_content.extend(special)

        if category_content:
            yield Horizontal(classes="category_horizontal", *category_content)
