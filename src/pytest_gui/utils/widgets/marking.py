import json
from collections.abc import Iterator
from pathlib import Path

from textual.widget import Widget
from textual.widgets import Label

from pytest_gui.logging import logger
from pytest_gui.utils.config import get_test_name_by_test_result
from pytest_gui.utils.test_results import TestResult, extract_marks_with_results
from pytest_gui.utils.types.config import Test, TestConfig
from pytest_gui.utils.types.widgets import WidgetsDict


def mark_widget_running(widget: Widget) -> None:
    widget.add_class("running")


def mark_widget_list_running(widget_list: list[Widget]) -> None:
    for widget in widget_list:
        mark_widget_running(widget)


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
                            widget.remove_class("passed")
                            widget.remove_class("failed")
                            widget.remove_class("skipped")
                else:
                    for widget in widget_list:
                        widget.remove_class("running")
                        widget.remove_class("passed")
                        widget.remove_class("failed")
                        widget.remove_class("skipped")


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

        get_widget_by_test_name(widgets, test_name, test_result)


def process_widget(widget: Widget, test_result: TestResult) -> None:
    outcome = test_result.outcome
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


def iter_tests(config_data: TestConfig) -> Iterator[Test]:
    """Yield all test definitions from config."""
    for category in config_data.get("categories", []):
        for subcat in category.get("subcategories", []):
            yield from subcat.get("tests", [])


def get_widget_by_test_name(widgets: WidgetsDict, test_name: str, test_result: TestResult) -> None:
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


def get_label_of_special_test_widget(widget: Widget) -> str | None:
    subcategory_content = widget.parent.parent.parent

    for w in subcategory_content.children:
        if isinstance(w, Label):
            return w.renderable

    logger.error(f"Label not found for special test widget {widget}.")
    return None


def parse_result_arg_values(args: str) -> list[str]:
    if not args:
        logger.error("No args to parse.")
        return []

    return [arg.strip() for arg in args.split("-")]


def args_match_widget_values(args: list[str], widgets: list[Widget]) -> bool:
    for i, widget in enumerate(widgets):
        if args[i] != widget.value:
            return False

    return True
