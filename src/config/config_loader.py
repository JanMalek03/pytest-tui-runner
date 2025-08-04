import json
from pathlib import Path

import yaml

from src.utils.types.config import TestConfig


def load_config(file_path: str) -> TestConfig:
    """Load and parses a configuration file.

    Parameters
    ----------
    file_path : str
        The path to the configuration file.

    Returns
    -------
    TestConfig
        An object representing the parsed test configuration.

    Raises
    ------
    FileNotFoundError
        If the configuration file does not exist.
    ValueError
        If the file format is not YAML or JSON.

    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Configuration file {file_path} does not exist.")

    if path.suffix in {".yaml", ".yml"}:
        with Path.open(path, encoding="utf-8") as file:
            return yaml.safe_load(file)
    elif path.suffix == ".json":
        with Path.open(path, encoding="utf-8") as file:
            return json.load(file)
    else:
        raise ValueError("Only YAML and JSON files are supported.")
