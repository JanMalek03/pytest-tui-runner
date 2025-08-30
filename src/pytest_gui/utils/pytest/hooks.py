from collections.abc import Iterator

from pytest_gui.utils.types.config import Test, TestConfig


def iter_tests(config_data: TestConfig) -> Iterator[Test]:
    """Yield all test definitions from config."""
    for category in config_data.get("categories", []):
        for subcat in category.get("subcategories", []):
            yield from subcat.get("tests", [])


def parse_variants(raw_value: str) -> list[dict[str, str]]:
    """
    Parse CLI argument string into list of dicts.

    Example:
      "action:Delete,image:123;action:Copy,image:456"
    → [{'action': 'Delete', 'image': '123'}, {'action': 'Copy', 'image': '456'}]
    """
    variants: list[dict[str, str]] = []
    for part in raw_value.split(";"):
        variant = {}
        for arg in part.split(","):
            key, value = arg.split(":")
            variant[key.strip()] = value.strip()
        variants.append(variant)
    return variants
