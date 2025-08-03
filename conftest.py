from pathlib import Path

import yaml

current_dir = Path(__file__).parent
FILE_PATH = current_dir / "tests" / "pytest_gui" / "default.yaml"


def pytest_addoption(parser) -> None:
    assert FILE_PATH.exists(), f"Configuration file {FILE_PATH} does not exist."
    with Path.open(FILE_PATH, encoding="utf-8") as file:
        config = yaml.safe_load(file)

    for category in config["categories"]:
        for subcat in category.get("subcategories", []):
            for test in subcat.get("tests", []):
                option_name = test_name_to_flag(test["name"])
                parser.addoption(
                    option_name,
                    action="store_true",
                    default=False,
                    help="Run login tests",
                )


def pytest_collection_modifyitems(config, items) -> None:
    selected_items = []

    with Path.open(FILE_PATH, encoding="utf-8") as file:
        config_data = yaml.safe_load(file)

    enabled_marker_sets = []

    for category in config_data["categories"]:
        for subcat in category.get("subcategories", []):
            for test_def in subcat.get("tests", []):
                option_name = test_name_to_flag(test_def["name"])
                if config.getoption(option_name):
                    enabled_marker_sets.append(frozenset(test_def["markers"]))

    for item in items:
        item_markers = {marker.name for marker in item.iter_markers()}

        if frozenset(item_markers) in enabled_marker_sets:
            selected_items.append(item)

    items[:] = selected_items


# def pytest_generate_tests(metafunc):
#     if "images" in metafunc.definition.keywords:
#         run_images = metafunc.config.getoption("--run-images")

#         if "mode" in metafunc.fixturenames and "image_name" in metafunc.fixturenames and run_images:
#             run_images_parts = run_images.split(";")

#             modes = []
#             images = []

#             for part in run_images_parts:
#                 print(part)
#                 if part.startswith("modes:"):
#                     modes = part[len("modes:"):].strip("[]").split(",")
#                     modes = [mode.strip() for mode in modes]
#                 elif part.startswith("images:"):
#                     images = part[len("images:"):].strip("[]").split(",")
#                     images = [image.strip() for image in images]

#             if "mode" in metafunc.fixturenames and "image_name" in metafunc.fixturenames:
#                 combinations = [(mode, image) for mode in modes for image in images]
#                 metafunc.parametrize("mode, image_name", combinations)


def test_name_to_flag(name: str) -> str:
    return f"--run-{name.replace(' ', '-').lower()}"
