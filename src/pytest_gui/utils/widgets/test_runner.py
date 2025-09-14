import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from textual.widget import Widget
from textual.widgets import Label

from pytest_gui.config import load_config
from pytest_gui.logging import logger
from pytest_gui.paths import Paths
from pytest_gui.utils.types.config import Test, TestConfig
from pytest_gui.utils.types.widgets import WidgetsDict

IGNORED_MARKERS = {"skip", "xfail"}


@dataclass
class TestResult:
    markers: list[str]
    outcome: str
    args: dict[str, str] | None = None


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


def extract_marks_with_results(report) -> list[TestResult]:
    tests_results: list[TestResult] = []

    tests = report.get("tests", [])
    for test in tests:
        test_result = test.get("outcome", "")
        keywords = test.get("keywords", [])

        if not keywords:
            logger.error("Test has no keywords.")
            continue

        # Extract test marks
        marks = []
        for kw in keywords[1:]:
            if kw == "pytestmark":
                break
            if kw in IGNORED_MARKERS:
                continue
            marks.append(kw)

        # Check if test (first keyword) is test with arguments (has format test_name[args])
        test_name = keywords[0]
        if "[" in test_name and test_name.endswith("]"):
            test_args = test_name.split("[", 1)[1][:-1]

            logger.debug(f"Test WITH' arguments found: '{test_name}'")
            tests_results.append(TestResult(markers=marks, outcome=test_result, args=test_args))
        else:
            logger.debug(f"Test WITHOUT arguments found: '{test_name}'")
            tests_results.append(TestResult(markers=marks, outcome=test_result))

    logger.debug(f"Test results extracted: {tests_results}")

    return tests_results


def get_test_name_by_test_result(result: TestResult) -> str | None:
    config_data: TestConfig = load_config(Paths.config())

    logger.debug(f"Searching: {result.markers}")

    for test_def in iter_tests(config_data):
        logger.debug(f"Comparing with: {test_def['markers']}")
        if frozenset(test_def["markers"]) == frozenset(result.markers):
            logger.debug(f"Match found: '{test_def['name']}'")
            return test_def["name"]

    logger.error("No matching test definition found.")

    return None


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
