from textual.widgets import Button


async def disable_buttons_after_test_runs(buttons: list[Button]) -> None:
    """Disable buttons to prevent multiple test runs."""
    for button in buttons:
        if button.id == "run_tests":
            button.disabled = True


async def enable_buttons_after_test_finnished(buttons: list[Button]) -> None:
    """Enable buttons after test run is finished."""
    for button in buttons:
        if button.id == "run_tests":
            button.disabled = False
