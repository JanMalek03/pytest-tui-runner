def pytest_addoption(parser):
    parser.addoption(
        "--run-login", action="store_true", default=False, help="Run login tests"
    )
    parser.addoption(
        "--run-navigation", action="store_true", default=False, help="Run navigation tests"
    )
    parser.addoption(
        "--run-images", action="store", nargs="?", default=None, help="Run image tests"
    )


def pytest_collection_modifyitems(config, items):
    run_login = config.getoption("--run-login")
    run_navigation = config.getoption("--run-navigation")
    run_images = config.getoption("--run-images")

    selected_items = []

    for item in items:
        if "login" in item.keywords and run_login:
            selected_items.append(item)
        elif "navigation" in item.keywords and run_navigation:
            selected_items.append(item)
        elif "images" in item.keywords and run_images is not None:
            selected_items.append(item)

    items[:] = selected_items


def pytest_generate_tests(metafunc):
    if "images" in metafunc.definition.keywords:
        run_images = metafunc.config.getoption("--run-images")

        if "mode" in metafunc.fixturenames and "image_name" in metafunc.fixturenames and run_images:
            run_images_parts = run_images.split(";")

            modes = []
            images = []

            for part in run_images_parts:
                print(part)
                if part.startswith("modes:"):
                    modes = part[len("modes:"):].strip("[]").split(",")
                    modes = [mode.strip() for mode in modes]
                elif part.startswith("images:"):
                    images = part[len("images:"):].strip("[]").split(",")
                    images = [image.strip() for image in images]

            if "mode" in metafunc.fixturenames and "image_name" in metafunc.fixturenames:
                combinations = [(mode, image) for mode in modes for image in images]
                metafunc.parametrize("mode, image_name", combinations)
