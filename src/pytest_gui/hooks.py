from pathlib import Path
from urllib.parse import unquote

import yaml
from _pytest.config.argparsing import Parser
from _pytest.python import Metafunc

from pytest_gui.config.paths import CONFIG_PATH
from pytest_gui.logs.logger_config import logger


def pytest_addoption(parser: Parser) -> None:
    assert CONFIG_PATH.exists(), f"Configuration file {CONFIG_PATH} does not exist."
    with Path.open(CONFIG_PATH, encoding="utf-8") as file:
        config = yaml.safe_load(file)

    for category in config["categories"]:
        for subcat in category.get("subcategories", []):
            for test in subcat.get("tests", []):
                option_name: str = test_name_to_flag(test["name"])

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
    with Path.open(CONFIG_PATH, encoding="utf-8") as file:
        config_data = yaml.safe_load(file)

    # Go through the options given by pytest so we know which tests to run
    enabled_marker_sets: list = []
    for category in config_data["categories"]:
        for subcat in category.get("subcategories", []):
            for test_def in subcat.get("tests", []):
                option_name: str = test_name_to_flag(test_def["name"])
                opt_value = config.getoption(option_name)
                if opt_value:
                    enabled_marker_sets.append(frozenset(test_def["markers"]))

    selected_tests: list = []
    for item in items:
        item_markers = {marker.name for marker in item.iter_markers()}

        if frozenset(item_markers) in enabled_marker_sets:
            selected_tests.append(item)

    # logger.critical("")
    logger.critical(enabled_marker_sets)
    logger.warning(selected_tests)

    items[:] = selected_tests


def pytest_generate_tests(metafunc: Metafunc) -> None:
    with Path.open(CONFIG_PATH, encoding="utf-8") as file:
        config_data = yaml.safe_load(file)

    # jmena markeru pro tento metafunc
    marker_names = {marker.name for marker in metafunc.definition.iter_markers()}

    for category in config_data["categories"]:
        for subcat in category.get("subcategories", []):
            for test_def in subcat.get("tests", []):
                if test_def["type"] != "special":
                    continue

                conf_markers = set(test_def.get("markers", []))
                # porovnat presna sada nebo subset (zvol dle potreby)
                if conf_markers != marker_names:
                    continue

                # nasli jsme config entry pro aktualni test
                option_name = test_name_to_flag(
                    test_def["name"],
                )  # musi odpovidat pytest_addoption
                raw_value = metafunc.config.getoption(option_name)

                if not raw_value:
                    # nebyla zadana CLI volba -> nic nedelame
                    return

                value = unquote(raw_value)

                variants: list[dict[str]] = []
                for arguments in value.split(";"):
                    arguments = arguments.split(",")

                    variant = {}
                    for argument in arguments:
                        key, value = argument.split(":")
                        variant[key.strip()] = value.strip()

                    variants.append(variant)

                # logger.critical(variants)
                # priklad result= [{'action': 'Delete image', 'image': '789'}, {'action': 'Add image', 'image': '123'}, {'action': 'Copy image', 'image': '456'}]

                if variants:
                    param_names = list(variants[0].keys())
                    param_values = [tuple(v[k] for k in param_names) for v in variants]

                    # logger.critical(param_names)
                    # logger.warning(param_values)

                    metafunc.parametrize(param_names, param_values)

                return


def test_name_to_flag(test_name: str) -> str:
    """Format test name into a pytest CLI flag."""
    # Example: "My Test" → "--run-my-test"
    return f"--run-{test_name.lower().replace(' ', '-')}"
