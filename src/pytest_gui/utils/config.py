from collections.abc import Iterator

from pytest_gui.config import load_config
from pytest_gui.logging import logger
from pytest_gui.paths import Paths
from pytest_gui.utils.test_results import TestResult
from pytest_gui.utils.types.config import Test, TestConfig


def iter_tests(config_data: TestConfig) -> Iterator[Test]:
    """Yield all test definitions from config."""
    for category in config_data.get("categories", []):
        for subcat in category.get("subcategories", []):
            yield from subcat.get("tests", [])


def get_test_name_by_test_result(result: TestResult) -> str | None:
    config_data: TestConfig = load_config(Paths.config())
    logger.debug(f"Searching: {result.markers}")

    for test_def in iter_tests(config_data):
        if frozenset(test_def["markers"]) == frozenset(result.markers):
            logger.debug(f"Match found: '{test_def['name']}'")
            return test_def["name"]

    logger.error("No matching test definition found.")
    return None
