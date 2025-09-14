from _pytest.config.argparsing import Parser
from _pytest.python import Metafunc

from pytest_gui.config import load_config
from pytest_gui.logging import logger, setup_logger
from pytest_gui.paths import Paths
from pytest_gui.utils.config import iter_tests
from pytest_gui.utils.pytest.arguments import format_test_flag
from pytest_gui.utils.pytest.encoding import decode_variants
from pytest_gui.utils.test_results import IGNORED_MARKERS
from pytest_gui.utils.types.config import TestConfig


def pytest_addoption(parser: Parser) -> None:
    # After running the test as a new process, it is necessary to set up the logger again.
    # This is the first function called when the test is run, so it's here
    setup_logger()
    logger.debug("---------------------------- PYTEST HOOKS ----------------------------")
    logger.debug("▶️ ADD OPTIONS hook")

    config: TestConfig = load_config(Paths.config())

    for test in iter_tests(config):
        option_name: str = format_test_flag(test["name"])

        # Special test with arguments
        if "arguments" in test:
            logger.debug(f"Adding option with arguments = '{option_name}'")
            parser.addoption(
                option_name,
                action="store",
                help=f"Run '{test['name']}' test with arguments",
            )
        else:
            logger.debug(f"Adding basic option = '{option_name}'")
            parser.addoption(
                option_name,
                action="store_true",
                default=False,
                help=f"Run '{test['name']}' test",
            )

    logger.debug("✅ ADD OPTIONS hook")


def pytest_generate_tests(metafunc: Metafunc) -> None:
    test_name = metafunc.function.__name__
    logger.debug(f"▶️ GENERATE TESTS hook for '{(test_name)}' test")

    config_data: TestConfig = load_config(Paths.config())
    marker_names: set[str] = {
        marker.name
        for marker in metafunc.definition.iter_markers()
        if marker.name not in IGNORED_MARKERS
    }

    try:
        for test_def in iter_tests(config_data):
            if test_def["type"] != "special":
                continue

            actual_markers = set(test_def.get("markers", []))

            if actual_markers != marker_names:
                logger.debug(f"This test has no expected marks ({test_def['name']})")
                logger.debug(f"Expected = {actual_markers}")
                logger.debug(f"Have = {marker_names}")
                continue

            logger.debug(f"'EXPECTED MARKS FOUND' = {marker_names}")

            option_name = format_test_flag(test_def["name"])
            raw_value = metafunc.config.getoption(option_name)

            if not raw_value:
                logger.error("No arguments value received")
                return

            variants: list[dict[str, str]] = decode_variants(raw_value)
            if not variants:
                logger.error("Argument decoding returned nothing")
                return

            param_names = list(variants[0].keys())
            param_values = [tuple(v[k] for k in param_names) for v in variants]

            logger.debug(f"Parameters names = {param_names}")
            logger.debug(f"Parameters values = {param_values}")

            logger.debug("Executing parametrize function")
            metafunc.parametrize(param_names, param_values)

    finally:
        logger.debug("✅ GENERATE TESTS hook")


def pytest_collection_modifyitems(config, items) -> None:
    logger.debug("▶️ COLLECTION MODIFYITEMS hook")
    logger.debug(f"Test count before filtering = {len(items)}")

    config_data: TestConfig = load_config(Paths.config())

    # Go through the options given by pytest so we know which tests to run
    enabled_marker_sets: list = []
    for test_def in iter_tests(config_data):
        logger.debug(f"Checking test '{test_def['name']}' if it has been selected")

        option_name: str = format_test_flag(test_def["name"])
        opt_value = config.getoption(option_name)
        if opt_value:
            logger.debug(f"Pytest argument found = '{opt_value}'")
            marks = frozenset(test_def["markers"])
            logger.debug(f"Adding marks to the list = {marks}")
            enabled_marker_sets.append(marks)
        else:
            logger.debug("No pytest argument was specified for this test.")
            logger.debug("'Skipping'")

    logger.debug(f"List of wanted marks = {enabled_marker_sets}")

    # Keep only selected tests
    logger.debug("▶️ Filtering tests...")
    filtered_items = []
    for item in items:
        item_marks = frozenset(m.name for m in item.iter_markers() if m.name not in IGNORED_MARKERS)

        if item_marks in enabled_marker_sets:
            logger.debug(f"Required marks found ({item_marks}), leaving the test")
            filtered_items.append(item)
        else:
            logger.debug("Test skipped")
            logger.debug(f"Expected marks = {sorted(map(list, enabled_marker_sets))}")
            logger.debug(f"Have = {sorted(item_marks)}")
    items[:] = filtered_items
    logger.debug("✅ Tests filtered")

    logger.debug(f"Test count after filtering = {len(items)}")
    logger.debug("✅ COLLECTION MODIFYITEMS hook")

    # This is the last function to run when preparing the test, hence this log
    logger.debug("---------------------------- PYTEST HOOKS ----------------------------")
