import json
from pathlib import Path
from typing import Any

import yaml


class ConfigLoader:

    @staticmethod
    def load_config(file_path: str) -> dict[str, Any]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Configuration file {file_path} does not exist.")

        if path.suffix == ".yaml" or path.suffix == ".yml":
            with open(path, encoding="utf-8") as file:
                return yaml.safe_load(file)
        elif path.suffix == ".json":
            with open(path, encoding="utf-8") as file:
                return json.load(file)
        else:
            raise ValueError("Only YAML and JSON files are supported.")
