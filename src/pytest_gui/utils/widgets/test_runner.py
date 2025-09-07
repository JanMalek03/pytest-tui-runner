import json
from pathlib import Path

from textual.widget import Widget

from pytest_gui.logging import logger
from pytest_gui.utils.types.widgets import WidgetsDict


def mark_widgets_running(widgets: WidgetsDict) -> None:
    """Označí všechny widgety jako 'běžící' (např. modře)."""
    for category in widgets.values():
        for subcategory in category.values():
            for widget_list in subcategory.values():
                if (
                    isinstance(widget_list, list)
                    and widget_list
                    and isinstance(widget_list[0], list)
                ):
                    for inner_list in widget_list:
                        for widget in inner_list:
                            widget.add_class("running")
                else:
                    for widget in widget_list:
                        widget.add_class("running")


def reset_widgets_style(widgets: WidgetsDict) -> None:
    """Vrátí widgety zpět do původního stylu (odstraní označení)."""
    for category in widgets.values():
        for subcategory in category.values():
            for widget_list in subcategory.values():
                if (
                    isinstance(widget_list, list)
                    and widget_list
                    and isinstance(widget_list[0], list)
                ):
                    for inner_list in widget_list:
                        for widget in inner_list:
                            widget.remove_class("running")
                else:
                    for widget in widget_list:
                        widget.remove_class("running")


def mark_widgets_from_report(widgets: WidgetsDict, report_path: Path) -> None:
    """Update widget styles based on pytest JSON report outcomes."""
    if not report_path.exists():
        raise FileNotFoundError(f"Report file not found: {report_path}")

    with Path.open(report_path, encoding="utf-8") as f:
        report = json.load(f)

    # test_results = {test["nodeid"]: test["outcome"] for test in report.get("tests", [])}

    marks_with_result = extract_marks_with_results(report)

    logger.debug(marks_with_result)

    # for category_dict in widgets.values():
    #     for subcategory_dict in category_dict.values():
    #         for widget_group in subcategory_dict.values():
    #             for widget in widget_group if isinstance(widget_group, list) else []:
    #                 if isinstance(widget, list):
    #                     for w in widget:
    #                         process_widget(w, test_results)
    #                 else:
    #                     process_widget(widget, test_results)


def process_widget(widget: Widget, test_results) -> None:
    test_id = getattr(widget, "test_nodeid", None)
    if not test_id:
        return

    outcome = test_results.get(test_id)
    if outcome == "passed":
        widget.add_class("passed")
    elif outcome == "failed":
        widget.add_class("failed")
    elif outcome == "skipped":
        widget.add_class("skipped")
    else:
        # Pokud test nebyl nalezen nebo outcome neznámý, odeber staré styly
        widget.remove_class("passed")
        widget.remove_class("failed")
        widget.remove_class("skipped")


def extract_marks_with_results(report):
    marks_with_result = []

    tests = report.get("tests", [])
    for test in tests:
        test_result = test.get("outcome", "")
        keywords = test.get("keywords", [])

        marks = []
        for kw in keywords[1:]:
            if kw == "pytestmark":
                break
            marks.append(kw)

        marks_with_result.append((marks, test_result))

    return marks_with_result
