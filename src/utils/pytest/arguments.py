from textual.widgets import Checkbox
from logs.logger_config import logger

def build_pytest_arguments(widgets, pytest_init_path = ""):
    # Default arguments to run pytest with uv
    args = ["uv", "run", "pytest"]

    # Custom pytest.ini path
    if pytest_init_path:
        args += ["-c", pytest_init_path]
    else:
        logger.debug("No custom pytest.ini path provided, using default.")

    # Additional arguments for pytest
    args += ["-s"] # -s for capturing output

    for cat, subcats in widgets.items():
        for subcat, tests in subcats.items():
            for test_name, widgets in tests.items():
                for widget in widgets:
                    if isinstance(widget, Checkbox) and widget.value:
                        test_name = str(widget.label)
                        args.append(f"--run-{test_name.lower().replace(' ', '-')}")

    logger.info(f"Built pytest arguments: {args}")

    return args
