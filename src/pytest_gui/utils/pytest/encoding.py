from urllib.parse import quote, unquote

from textual.widget import Widget
from textual.widgets import Select

from pytest_gui.logging import logger
from pytest_gui.utils.types.widgets import TestArguments

VARIANT_SEP = ";"
PAIR_SEP = ","
KV_SEP = ":"


def encode_variants(test_name: str, variants: list[TestArguments]) -> str | None:
    """
    Encode list of variant dicts into a single string.

    Example:
      [{'action': 'Delete', 'image': '123'}, {'action': 'Copy', 'image': '456'}]
    → "action:Delete,image:123;action:Copy,image:456"
    """
    encoded_variants: list[str] = []
    had_any_value = False
    missing_value = False
    last_missing_widget: Widget | None = None

    for widget_list in variants:
        parts: list[str] = []
        for widget in widget_list:
            if hasattr(widget, "name") and hasattr(widget, "value"):
                if widget.value in (None, "", Select.BLANK):
                    missing_value = True
                    last_missing_widget = widget
                    continue
                had_any_value = True
                name: str = quote(str(widget.name), safe="")
                value: str = quote(str(widget.value), safe="")
                parts.append(f"{name}{KV_SEP}{value}")
        if parts:
            encoded_variants.append(PAIR_SEP.join(parts))

    if not had_any_value:
        return None

    if missing_value:
        logger.debug(f"Value for widget '{last_missing_widget.name}' is not set.")
        logger.warning(f"Skipping test '{test_name}'")
        return None

    return VARIANT_SEP.join(encoded_variants)


def decode_variants(raw_value: str) -> list[TestArguments]:
    """
    Decode CLI argument string back into list of dicts.

    Example:
      "action:Delete,image:123;action:Copy,image:456"
    → [{'action': 'Delete', 'image': '123'}, {'action': 'Copy', 'image': '456'}]
    """
    variants: list[TestArguments] = []
    for part in raw_value.split(VARIANT_SEP):
        if not part.strip():
            continue
        variant = {}
        for arg in part.split(PAIR_SEP):
            if not arg.strip():
                continue
            key, value = arg.split(KV_SEP, 1)
            variant[unquote(key.strip())] = unquote(value.strip())
        variants.append(variant)
    return variants
