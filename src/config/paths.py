from pathlib import Path

def find_project_root(start_path: Path = Path(__file__).resolve()) -> Path:
    for parent in [start_path, *start_path.parents]:
        if (parent / "README.md").is_file():
            return parent
    raise RuntimeError("ROOT_DIR not found - missing README.md")

ROOT_DIR = find_project_root()

# TEST_PATH="C:/_SCHOOL/Bakalarka/project_with_tests"
TEST_PATH="N:/SKOLA/Bakalarka/project_with_tests"
TEST_PATH = Path(TEST_PATH).resolve()

# CONFIG_PATH = ROOT_DIR / "src" / "config" / "default.yaml"
CONFIG_PATH = TEST_PATH / "tests" / "pytest_gui" / "default.yaml"
STATE_PATH = ROOT_DIR / "data" / "widgets_state.json"

PYTEST_INI_PATH = ROOT_DIR / "pytest.ini"

# LOG_DIR = ROOT_DIR / "logs"
LOG_DIR = TEST_PATH / "tests" / "pytest_gui" / "logs"
LOG_FILE = LOG_DIR / "app.log"
