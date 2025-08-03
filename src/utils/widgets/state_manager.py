import json

from textual.widgets import Checkbox


def load_widget_state(widgets, filename):
    with open(filename, encoding="utf-8") as f:
        saved = json.load(f)

    for cat, subcats in widgets.items():
        for subcat, tests in subcats.items():
            for test_name, widget_list in tests.items():
                if len(widget_list) == 1 and isinstance(widget_list[0], Checkbox):
                    widget_list[0].value = saved[cat][subcat][test_name][0]
                else:
                    for i, widgets in enumerate(widget_list):
                        for widget in widgets:
                            widget.value = saved[cat][subcat][test_name][i][widget.name]


def save_widget_state(widgets, filename):
    saved = {}

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
                            widget_data[instance.name] = instance.value

                        saved[cat][subcat][test_name].append(widget_data)


    with open(filename, "w", encoding="utf-8") as f:
        json.dump(saved, f, indent=2)


def is_boolean_list(value):
    return isinstance(value, list) and len(value) == 1 and isinstance(value[0], bool)
