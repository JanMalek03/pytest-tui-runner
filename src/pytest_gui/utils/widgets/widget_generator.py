from pathlib import Path

from textual.widget import Widget
from textual.widgets import Checkbox, Input, Select

from pytest_gui.utils.types.config import Argument, ArgumentType, Test, TestConfig, TestType
from pytest_gui.utils.types.saved_state import SavedState, SavedSubcat, TestValue
from pytest_gui.utils.types.widgets import WidgetsDict
from pytest_gui.utils.widgets.state_manager import read_json_state_file


def generate_widgets_from_config(config: TestConfig, state_path: Path | None = None) -> WidgetsDict:
    """
    Generate a nested dictionary of widgets from the given test configuration.

    Args:
        config: Test configuration loaded from YAML/JSON.
        state_path: Optional path to saved widget state.

    Returns
    -------
        Nested dict in the form:
        {
            category: {
                subcategory: {
                    test_name: widget | list[widget]
                }
            }
        }
    """
    saved_state: SavedState = read_json_state_file(state_path)
    widgets: WidgetsDict = {}

    for category in config["categories"]:
        cat_name: str = category["name"]
        widgets[cat_name] = {}

        for subcat in category.get("subcategories", []):
            subcat_name: str = subcat["name"]
            widgets[cat_name][subcat_name] = {}

            for test in subcat.get("tests", []):
                widgets[cat_name][subcat_name][test["name"]] = _create_test_widgets(
                    test,
                    saved_state.get(cat_name, {}).get(subcat_name, {}),
                )

    return widgets


def _create_test_widgets(test: Test, saved_subcat: SavedSubcat) -> list[Widget]:
    """Create a list of widgets by test type."""
    test_type: TestType = test.get("type")

    if test_type == "normal":
        return [Checkbox(test["name"])]

    if test_type == "special":
        # Get the number of saved states of the test argument
        saved_group: TestValue = saved_subcat.get(test["name"], [])
        num_groups: int = max(1, len(saved_group))

        return [_create_widgets_from_arguments(test["arguments"]) for _ in range(num_groups)]

    return []


def _create_widgets_from_arguments(arguments: list[Argument]) -> list[Widget]:
    """Create a list of widgets from a test's argument definitions."""
    result: list[Widget] = []
    for arg in arguments:
        widget: Widget | None = _widget_from_argument(arg)
        if widget is not None:
            result.append(widget)
    return result


def _widget_from_argument(arg: Argument) -> Widget | None:
    """Create a single widget based on argument definition."""
    arg_type: ArgumentType = arg.get("arg_type")
    if arg_type == "select":
        return Select(
            [(opt, opt) for opt in arg["options"]],
            allow_blank=True,
            name=arg["name"],
        )
    if arg_type == "text_input":
        return Input(
            placeholder=arg.get("placeholder", ""),
            name=arg["name"],
        )
    return None
