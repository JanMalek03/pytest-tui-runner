from textual.widget import Widget
from textual.widgets import Checkbox

from pytest_gui.logging import logger
from pytest_gui.utils.pytest.encoding import encode_variants
from pytest_gui.utils.types.widgets import TestArguments, WidgetsDict


def build_pytest_arguments(widgets: dict, pytest_init_path: str = "") -> list[str]:
    """Build a list of arguments for running pytest based on provided widgets and an optional pytest.ini path.

    Parameters
    ----------
    widgets : dict
        Dictionary containing widget objects organized by categories and subcategories.
    pytest_init_path : str, optional
        Path to a custom pytest.ini file (default is "")

    Returns
    -------
    list[str]
        List of command-line arguments for pytest.

    """
    # Default arguments to run pytest with uv
    args: list[str] = ["uv", "run", "pytest"]

    # Custom pytest.ini path
    if pytest_init_path:
        args += ["-c", pytest_init_path]
    else:
        logger.debug("No custom pytest.ini path provided, using default.")

    # Additional arguments for pytest
    args += ["-s"]  # -s for capturing output

    # Add widget-derived arguments
    args.extend(extract_widget_arguments(widgets))

    logger.info(f"Built pytest arguments: {args}")
    return args


def extract_widget_arguments(widgets: WidgetsDict) -> list[str]:
    """Extract pytest CLI arguments from widget states."""
    args: list[str] = []
    for subcats in widgets.values():
        for tests in subcats.values():
            for test_name, widget_list in tests.items():
                # Check if widget_list contains arguments for the test
                if isinstance(widget_list[0], list):
                    arg: str | None = widget_to_argument(test_name, widget_list)
                    if arg:
                        args.append(arg)
                else:
                    for widget in widget_list:
                        arg: str | None = widget_to_argument(test_name, widget)
                        if arg:
                            args.append(arg)
    return args


def widget_to_argument(test_name: str, widgets: Widget | list[TestArguments]) -> str | None:
    """Convert a widget into a pytest CLI argument, if applicable."""
    # Basic Checkbox type test
    if isinstance(widgets, Checkbox) and widgets.value:
        return format_test_flag(str(widgets.label))

    if isinstance(widgets, list) and widgets:
        variant_strings: str = encode_variants(test_name, widgets)
        if variant_strings is not None:
            return f"{format_test_flag(test_name)}=" + variant_strings

    return None


def format_test_flag(test_name: str) -> str:
    """Format test name into a pytest CLI flag."""
    # Example: "My Test" → "--run-my-test"
    return f"--run-{test_name.lower().replace(' ', '-')}"
