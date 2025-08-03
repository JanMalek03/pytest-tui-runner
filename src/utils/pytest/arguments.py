from textual.widgets import Checkbox

from logs.logger_config import logger


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

    for subcats in widgets.values():
        for tests in subcats.values():
            for test_name, widgets in tests.items():
                for widget in widgets:
                    if isinstance(widget, Checkbox) and widget.value:
                        test_name = str(widget.label)
                        args.append(f"--run-{test_name.lower().replace(' ', '-')}")

    logger.info(f"Built pytest arguments: {args}")

    return args
