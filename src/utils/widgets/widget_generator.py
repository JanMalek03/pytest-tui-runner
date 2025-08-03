import json
from pathlib import Path

from textual.widgets import Checkbox, Input, Select

from logs.logger_config import logger


def generate_widgets_from_config(config: dict, state_path: str = None) -> dict:
    if state_path:
        with Path.open(state_path, encoding="utf-8") as f:
            saved = json.load(f)
            if not saved:
                logger.warning("No saved state found, generating widgets from config only.")

    widgets: dict = {}

    for category in config["categories"]:
        cat_name = category["name"]
        widgets[cat_name] = {}

        for subcat in category.get("subcategories", []):
            subcat_name = subcat["name"]
            widgets[cat_name][subcat_name] = {}

            for test in subcat.get("tests", []):
                test_name = test["name"]
                if test["type"] == "special":
                    special_group = [
                        _create_widgets_for_test(test)
                        for _ in range(len(saved[cat_name][subcat_name][test_name]))
                    ]
                    widgets[cat_name][subcat_name][test_name] = special_group
                else:
                    widgets[cat_name][subcat_name][test_name] = _create_widgets_for_test(test)

    return widgets


def _create_widgets_for_test(test):
    if test["type"] == "normal":
        return [Checkbox(test["name"])]
    if test["type"] == "special":
        return [_widget_from_argument(arg) for arg in test["arguments"]]
    return []


def _widget_from_argument(arg):
    if arg["arg_type"] == "select":
        return Select([(opt, opt) for opt in arg["options"]], allow_blank=False, name=arg["name"])
    if arg["arg_type"] == "text_input":
        return Input(placeholder=arg.get("placeholder", ""), name=arg["name"])
    return None
