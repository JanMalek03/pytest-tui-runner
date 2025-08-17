from pathlib import Path

from _pytest.config.argparsing import Parser
from _pytest.python import Metafunc

FILE_PATH: Path = Path(__file__).parent / "default.yaml"


def pytest_addoption(parser: Parser) -> None:
    # ...
    pass


def pytest_collection_modifyitems(config, items) -> None:
    # ...
    pass


def pytest_generate_tests(metafunc: Metafunc) -> None:
    # ...
    pass
