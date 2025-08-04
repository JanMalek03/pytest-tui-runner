import json
from pathlib import Path

from textual.widgets import Checkbox, Select

from logs.logger_config import logger


def load_widget_state(widgets: dict, filename: str) -> None:
    try:
        with Path.open(filename, encoding="utf-8") as f:
            saved = json.load(f)
    except Exception as e:
        logger.error(f"An error occurred while loading saved data: {e}", exc_info=True)
        saved = {}

    for cat, subcats in widgets.items():
        for subcat, tests in subcats.items():
            for test_name, widget_list in tests.items():
                if len(widget_list) == 1 and isinstance(widget_list[0], Checkbox):
                    if widget_list:
                        test_data = saved.get(cat, {}).get(subcat, {}).get(test_name, [])
                        if test_data:
                            widget_list[0].value = test_data[0]
                else:
                    for i, widgets in enumerate(widget_list):
                        for widget in widgets:
                            group_list = saved.get(cat, {}).get(subcat, {}).get(test_name, [])
                            if i < len(group_list):
                                try:
                                    widget.value = group_list[i].get(widget.name)
                                except Exception as e:
                                    logger.error(
                                        f"Error reading widget value: {e}",
                                        exc_info=True,
                                    )


def save_widget_state(widgets: dict, filename: str) -> None:
    saved: dict = {}

    for cat, subcats in widgets.items():
        saved[cat] = {}
        for subcat, tests in subcats.items():
            saved[cat][subcat] = {}
            for test_name, widget_list in tests.items():
                saved[cat][subcat][test_name] = []

                for widget in widget_list:
                    if isinstance(widget, Checkbox):
                        saved[cat][subcat][test_name].append(widget.value)
                    else:
                        widget_data = {}

                        for instance in widget:
                            if instance.value == Select.BLANK:
                                widget_data[instance.name] = ""
                            else:
                                widget_data[instance.name] = instance.value

                        saved[cat][subcat][test_name].append(widget_data)

    with Path.open(filename, "w", encoding="utf-8") as f:
        json.dump(saved, f, indent=2)
