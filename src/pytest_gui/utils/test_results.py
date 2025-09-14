from dataclasses import dataclass

from pytest_gui.logging import logger

IGNORED_MARKERS = {"skip", "xfail"}


@dataclass
class TestResult:
    """Represents the result of a test with its markers and outcome."""

    markers: list[str]
    outcome: str
    args: dict[str, str] | None = None


def extract_marks_with_results(report) -> list[TestResult]:
    """Extract test results and their markers from a pytest JSON report."""
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
