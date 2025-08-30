import os
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


def find_project_root_by_tests(start: Path) -> Path | None:
    current = start.resolve()
    for parent in [current] + list(current.parents):
        # TODO: mozna pridat vice moznosti, treba tests or README, nebo tak
        if (parent / "tests").is_dir():
            return parent
    return None


class Paths:
    """Central place for all important paths."""

    # root of *this* package
    ROOT_DIR: Path = find_project_root()

    # user project root (to be set dynamically from CLI)
    _user_root: Path | None = None

    # ------------------ SET/GET ------------------

    @classmethod
    def set_user_root(cls, path: Path) -> None:
        cls._user_root = path.resolve()

    @classmethod
    def user_root(cls) -> Path:
        if cls._user_root is not None:
            return cls._user_root

        env_root = os.getenv("PYTEST_GUI_ROOT")
        if env_root:
            return Path(env_root).resolve()

        raise RuntimeError("User project root is not set yet.")

    # ------------------ USER-DEPENDENT PATHS ------------------

    @classmethod
    def config(cls) -> Path:
        return cls.user_root() / "pytest_gui" / "default.yaml"

    @classmethod
    def log_dir(cls) -> Path:
        return cls.user_root() / "pytest_gui" / "logs"

    @classmethod
    def state_file(cls) -> Path:
        return cls.user_root() / "pytest_gui" / "widgets_state.json"

    @classmethod
    def log_file(cls) -> Path:
        return cls.log_dir() / "app.log"

    # ------------------ PACKAGE-INTERNAL PATHS ------------------

    @classmethod
    def pytest_ini(cls) -> Path:
        return cls.ROOT_DIR / "pytest.ini"
