import json
from textual.widgets import Select, Checkbox
from logs.logger_config import logger

def load_widget_state(widgets, filename):
    with open(filename, "r", encoding="utf-8") as f:
        saved = json.load(f)

    for cat, subcats in widgets.items():
        for subcat, tests in subcats.items():
            # logger.critical(tests)
            for test_name, widget_list in tests.items():
                if len(widget_list) == 1 and isinstance(widget_list[0], Checkbox):
                    widget_list[0].value = saved[cat][subcat][test_name][0]
                else:
                    pass
                    # logger.warning(widget_list)
                    # for widget in widget_list:
                    #     if widget.name in saved[cat][subcat][test_name][i]:
                    #         val = saved[cat][subcat][test_name][i][widget.name]
                    #         logger.warning(saved[cat][subcat][test_name][i][widget.name])
                    #     else:
                    #         logger.error(f"Widget {widget.name} not found in saved state for {cat}/{subcat}/{test_name}.")
                    #         continue
                    #     widget.value = val


def save_widget_state(widgets, filename):
    saved = {}

    for cat, subcats in widgets.items():
        saved[cat] = {}
        for subcat, tests in subcats.items():
            saved[cat][subcat] = {}
            for test_name, widget_list in tests.items():
                saved[cat][subcat][test_name] = []
                group = {}
                for widget in widget_list:
                    val = "" if widget.value == Select.BLANK else widget.value

                    if isinstance(widget, Checkbox):
                        saved[cat][subcat][test_name].append(val)
                    else:
                        # if widgets are repeating, start a new group
                        if group and widget.name in group:
                            saved[cat][subcat][test_name].append(group)
                            group = {}

                        group[widget.name] = val
                
                if group:
                    saved[cat][subcat][test_name].append(group)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(saved, f, indent=2)


def is_boolean_list(value):
    return isinstance(value, list) and len(value) == 1 and isinstance(value[0], bool)
