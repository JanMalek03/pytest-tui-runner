import json
from pathlib import Path

import yaml

from pytest_gui.logging import logger
from pytest_gui.utils.types.config import TestConfig


def load_config(file_path: str) -> TestConfig:
    # TODO: add json as config. Now there is no json file to be loaded
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
        logger.error(f"Config file path does not exists: {file_path}")
        raise FileNotFoundError(f"Configuration file '{file_path}' does not exist")

    logger.debug(f"Config file path set to: '{file_path}'")

    if path.suffix in {".yaml", ".yml"}:
        logger.debug("Opening config file as a 'yaml' file")
        with Path.open(path, encoding="utf-8") as file:
            return yaml.safe_load(file)
    elif path.suffix == ".json":
        logger.debug("Opening config file as a 'json' file")
        with Path.open(path, encoding="utf-8") as file:
            return json.load(file)
    else:
        logger.error(f"Invalid config file format: '{path.suffix}'")
        raise ValueError("Only YAML and JSON files are supported.")
