import json
from pathlib import Path

from textual.widgets import Checkbox, Select

from logs.logger_config import logger
from src.pytest_gui.utils.types.saved_state import SavedState, TestState, TestValue
from src.pytest_gui.utils.types.widgets import TestWidgets, WidgetsDict


def load_widget_state(widgets: WidgetsDict, filename: Path) -> None:
    """Retrieve the state of the widgets from the JSON file and set the values for the existing widgets."""
    saved: SavedState = read_json_state_file(filename)

    for cat, subcats in widgets.items():
        for subcat, tests in subcats.items():
            for test_name, test_widgets in tests.items():
                saved_value: TestValue = _get_saved_value(saved, cat, subcat, test_name)
                _set_widgets_values(test_widgets, saved_value)


def save_widget_state(widgets: WidgetsDict, filename: Path) -> None:
    """Save the state of the widgets from the JSON file."""
    saved: SavedState = {}

    for cat, subcats in widgets.items():
        saved[cat] = {}
        for subcat, tests in subcats.items():
            saved[cat][subcat] = {}
            for test_name, test_widgets in tests.items():
                saved[cat][subcat][test_name] = _serialize_test_widgets(test_widgets)

    write_json_state_file(filename, saved)


def read_json_state_file(filename: Path) -> SavedState:
    """Load saved widget states from file and return as a dictionary."""
    if not filename:
        return {}
    try:
        with Path.open(filename, encoding="utf-8") as f:
            data: SavedState = json.load(f)
            if not data:
                logger.warning("No saved state found.")
            return data
    except Exception as e:
        logger.error(f"An error occurred while loading saved data: {e}", exc_info=True)
        return {}


def write_json_state_file(filename: Path, data: SavedState) -> None:
    """Write widget states data to a JSON file."""
    try:
        with Path.open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"An error occurred while saving data: {e}", exc_info=True)


def _get_saved_value(saved: SavedState, cat: str, subcat: str, test: str) -> TestValue:
    """Safely returns the saved list of values for the given test."""
    return saved.get(cat, {}).get(subcat, {}).get(test, [])


def _set_widgets_values(test_widgets: TestWidgets, saved_values: TestValue) -> None:
    """Retrieve widget values from stored data."""
    # Simple checkbox
    if _test_value_is_checkbox(test_widgets):
        if saved_values:
            try:
                test_widgets[0].value = saved_values[0]
            except Exception as e:
                logger.error(f"Error setting checkbox value: {e}", exc_info=True)
        return

    # Widget group (for test arguments)
    for i, arguments_widgets in enumerate(test_widgets):
        if i >= len(saved_values):
            continue
        for widget in arguments_widgets:
            try:
                widget.value = saved_values[i].get(widget.name)
            except Exception as e:
                logger.error(f"Error setting widget value: {e}", exc_info=True)


def _serialize_test_widgets(widget_group: TestWidgets) -> TestValue:
    """Convert widgets to a suitable structure for saving to a file."""
    if _test_value_is_checkbox(widget_group):
        return [widget_group[0].value]

    result: TestValue = []
    for widgets in widget_group:
        widget_data: TestState = {}
        for instance in widgets:
            widget_data[instance.name] = "" if instance.value == Select.BLANK else instance.value
        result.append(widget_data)
    return result


def _test_value_is_checkbox(test_widgets: TestWidgets) -> bool:
    """Check if they are widgets for checkbox type test or not."""
    # Widgets for the checkbox type test have only one element in the list, the checkbox widget
    return len(test_widgets) == 1 and isinstance(test_widgets[0], Checkbox)
