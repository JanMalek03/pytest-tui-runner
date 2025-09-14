import json
from pathlib import Path

from textual.widget import Widget
from textual.widgets import Label

from pytest_gui.logging import logger
from pytest_gui.utils.config import get_test_name_by_test_result
from pytest_gui.utils.test_results import TestResult, extract_marks_with_results
from pytest_gui.utils.types.widgets import WidgetsDict


def reset_widgets_style(widgets: WidgetsDict) -> None:
    """Remove marks from widgets."""
    for category in widgets.values():
        for subcategory in category.values():
            for widget_list in subcategory.values():
                if (
                    isinstance(widget_list, list)
                    and widget_list
                    and isinstance(widget_list[0], list)
                ):
                    for inner_list in widget_list:
                        reset_widget_list(inner_list)
                else:
                    reset_widget_list(widget_list)


def mark_widgets_from_report(widgets: WidgetsDict, report_path: Path) -> None:
    """Update widget styles based on pytest JSON report outcomes."""
    if not report_path.exists():
        raise FileNotFoundError(f"Report file not found: {report_path}")

    with Path.open(report_path, encoding="utf-8") as f:
        report = json.load(f)

    test_results = extract_marks_with_results(report)

    for test_result in test_results:
        test_name = get_test_name_by_test_result(test_result)
        if not test_name:
            continue

        mark_widgets_based_on_test_result(widgets, test_name, test_result)


def mark_widgets_based_on_test_result(
    widgets: WidgetsDict,
    test_name: str,
    test_result: TestResult,
) -> None:
    """Find and process the widget corresponding to the given test name and result."""
    logger.debug(f"Looking for widget with test name '{test_name}'")

    for category in widgets.values():
        for subcategory in category.values():
            for widget_list in subcategory.values():
                if (
                    isinstance(widget_list, list)
                    and widget_list
                    and isinstance(widget_list[0], list)
                ):
                    for inner_list in widget_list:
                        # TODO: inner_list muze byt jen widget
                        widget_sample = inner_list[0]
                        label = get_label_of_special_test_widget(widget_sample)
                        if label != test_name:
                            continue

                        parsed_args = parse_result_arg_values(test_result.args)
                        if args_match_widget_values(parsed_args, inner_list):
                            for widget in inner_list:
                                process_widget(widget, test_result)
                else:
                    for widget in widget_list:
                        if getattr(widget, "label", None) == test_name:
                            process_widget(widget, test_result)
                            return


def mark_widget_running(widget: Widget) -> None:
    """Mark widget as running."""
    widget.add_class("running")


def mark_widget_list_running(widget_list: list[Widget]) -> None:
    """Mark all widgets as running."""
    for widget in widget_list:
        mark_widget_running(widget)


def reset_widget_list(widgets: list[Widget]) -> None:
    """Remove all marks from widgets."""
    for widget in widgets:
        widget.remove_class("running")
        widget.remove_class("passed")
        widget.remove_class("failed")
        widget.remove_class("skipped")


def process_widget(widget: Widget, test_result: TestResult) -> None:
    """Update widget style based on test result."""
    outcome = test_result.outcome
    if outcome == "passed":
        widget.add_class("passed")
    elif outcome == "failed":
        widget.add_class("failed")
    elif outcome == "skipped":
        widget.add_class("skipped")
    else:
        widget.remove_class("passed")
        widget.remove_class("failed")
        widget.remove_class("skipped")


def get_label_of_special_test_widget(widget: Widget) -> str | None:
    """Get the label text of a special test widget."""
    subcategory_content = widget.parent.parent.parent

    for w in subcategory_content.children:
        if isinstance(w, Label):
            return w.renderable

    logger.error(f"Label not found for special test widget {widget}.")
    return None


def parse_result_arg_values(args: str) -> list[str]:
    """Parse argument values from test result args string."""
    if not args:
        logger.error("No args to parse.")
        return []

    return [arg.strip() for arg in args.split("-")]


def args_match_widget_values(args: list[str], widgets: list[Widget]) -> bool:
    """Check if argument values match the values of the given widgets."""
    return all(i < len(args) and args[i] == widget.value for i, widget in enumerate(widgets))
