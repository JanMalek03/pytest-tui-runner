from pathlib import Path


def find_project_root(start_path: Path | None = None) -> Path:
    """Recursively searches for the root of the project by locating a README.md file.

    Parameters
    ----------
    start_path : Path | None
        The starting path to begin the search. If None, uses the path of the current file.

    Returns
    -------
    Path
        The path to the root of the project.

    Raises
    ------
    RuntimeError
        If no directory with "README.md" is found in the hierarchy.
    """
    if start_path is None:
        start_path = Path(__file__).resolve()

    for parent in [start_path, *start_path.parents]:
        if (parent / "README.md").is_file():
            return parent
    raise RuntimeError("ROOT_DIR not found - missing README.md")


ROOT_DIR: Path = find_project_root()

# TEST_PATH="C:/_SCHOOL/Bakalarka/project_with_tests"
TEST_PATH = "N:/SKOLA/Bakalarka/project_with_tests"
TEST_PATH: Path = Path(TEST_PATH).resolve()

# CONFIG_PATH = ROOT_DIR / "src" / "config" / "default.yaml"
CONFIG_PATH: Path = TEST_PATH / "tests" / "pytest_gui" / "default.yaml"
# TODO: change so it works in package
STATE_PATH: Path = ROOT_DIR / "src" / "pytest_gui" / "widgets_state.json"

PYTEST_INI_PATH: Path = ROOT_DIR / "pytest.ini"

# LOG_DIR = ROOT_DIR / "logs"
LOG_DIR: Path = TEST_PATH / "tests" / "pytest_gui" / "logs"
LOG_FILE: Path = LOG_DIR / "app.log"
