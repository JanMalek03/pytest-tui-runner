from typing import TYPE_CHECKING
from urllib.parse import unquote

from _pytest.config.argparsing import Parser
from _pytest.python import Metafunc

from pytest_gui.config import load_config
from pytest_gui.logging import logger  # noqa: F401
from pytest_gui.paths import Paths
from pytest_gui.utils.pytest.arguments import format_test_flag
from pytest_gui.utils.pytest.hooks import iter_tests, parse_variants

if TYPE_CHECKING:
    from pytest_gui.utils.types.config import TestConfig


def pytest_addoption(parser: Parser) -> None:
    config: TestConfig = load_config(Paths.config())

    for test in iter_tests(config):
        option_name: str = format_test_flag(test["name"])

        # Special test with arguments
        if "arguments" in test:
            parser.addoption(
                option_name,
                action="store",
                help=f"Run '{test['name']}' test with arguments",
            )
        else:
            parser.addoption(
                option_name,
                action="store_true",
                default=False,
                help=f"Run '{test['name']}' test",
            )


def pytest_collection_modifyitems(config, items) -> None:
    config_data: TestConfig = load_config(Paths.config())

    # Go through the options given by pytest so we know which tests to run
    enabled_marker_sets: list = []
    for test_def in iter_tests(config_data):
        option_name: str = format_test_flag(test_def["name"])
        opt_value = config.getoption(option_name)
        if opt_value:
            enabled_marker_sets.append(frozenset(test_def["markers"]))

    # Keep only selected tests
    items[:] = [
        item
        for item in items
        if frozenset(m.name for m in item.iter_markers()) in enabled_marker_sets
    ]


def pytest_generate_tests(metafunc: Metafunc) -> None:
    config_data: TestConfig = load_config(Paths.config())
    marker_names: set[str] = {marker.name for marker in metafunc.definition.iter_markers()}

    for test_def in iter_tests(config_data):
        if test_def["type"] != "special":
            continue

        if set(test_def.get("markers", [])) != marker_names:
            continue

        option_name = format_test_flag(test_def["name"])
        raw_value = metafunc.config.getoption(option_name)
        if not raw_value:
            return

        variants: list[dict[str, str]] = parse_variants(unquote(raw_value))
        if not variants:
            return

        param_names = list(variants[0].keys())
        param_values = [tuple(v[k] for k in param_names) for v in variants]
        metafunc.parametrize(param_names, param_values)
        return
