from textual.widgets import Checkbox, Input, Select

def generate_widgets_from_config(config):
    widgets = {}

    for category in config["categories"]:
        cat_name = category["name"]
        widgets[cat_name] = {}

        for subcat in category.get("subcategories", []):
            subcat_name = subcat["name"]
            widgets[cat_name][subcat_name] = {}

            for test in subcat.get("tests", []):
                test_name = test["name"]
                widgets[cat_name][subcat_name][test_name] = _create_widgets_for_test(test)

    return widgets


def _create_widgets_for_test(test):
    if test["type"] == "normal":
        return [Checkbox(test["name"])]
    elif test["type"] == "special":
        return [_widget_from_argument(arg) for arg in test["arguments"]]
    return []


def _widget_from_argument(arg):
    if arg["arg_type"] == "select":
        return Select([(opt, opt) for opt in arg["options"]], allow_blank=False, name=arg["name"])
    elif arg["arg_type"] == "text_input":
        return Input(placeholder=arg.get("placeholder", ""), name=arg["name"])
    return None
