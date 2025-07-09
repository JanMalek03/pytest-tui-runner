import json
from textual.widgets import Select

def load_widget_state(widgets, filename):
    with open(filename, "r", encoding="utf-8") as f:
        saved = json.load(f)

    for cat, subcats in widgets.items():
        for subcat, tests in subcats.items():
            for test_name, widget_list in tests.items():
                for i, widget in enumerate(widget_list):
                    val = saved[cat][subcat][test_name][i][1]
                    widget.value = val


def save_widget_state(widgets, filename):
    saved = {}

    for cat, subcats in widgets.items():
        saved[cat] = {}
        for subcat, tests in subcats.items():
            saved[cat][subcat] = {}
            for test_name, widget_list in tests.items():
                saved[cat][subcat][test_name] = []
                for widget in widget_list:
                    val = None if widget.value == Select.BLANK else widget.value
                    saved[cat][subcat][test_name].append((widget.name, val))

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(saved, f, indent=2)
