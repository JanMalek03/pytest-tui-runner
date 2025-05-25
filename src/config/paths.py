from pathlib import Path

def find_project_root(start_path: Path = Path(__file__).resolve()) -> Path:
    for parent in [start_path, *start_path.parents]:
        if (parent / "README.md").is_file():
            return parent
    raise RuntimeError("ROOT_DIR not found – missing README.md")

ROOT_DIR = find_project_root()

CONFIG_PATH = ROOT_DIR / "src" / "config" / "default.yaml"
STATE_PATH = ROOT_DIR / "data" / "widgets_state.json"

LOG_DIR = ROOT_DIR / "logs"
LOG_FILE = LOG_DIR / "app.log"
