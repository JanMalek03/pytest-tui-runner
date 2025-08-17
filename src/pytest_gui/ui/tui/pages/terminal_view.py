from collections.abc import Iterator

from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import RichLog


class TerminalView(Vertical):
    """A page for displaying terminal output using RichLog in a vertical container."""

    def compose(self) -> Iterator[Widget]:
        """Compose the widgets for the tests view, including the scrollable test widgets and control buttons.

        Yields
        ------
        Widget
            The scrollable container of test widgets and the horizontal container of control buttons.

        """
        yield RichLog(id="pytest_log", highlight=True, wrap=True)

    def write_line(self, line: str) -> None:
        """Write a line to the RichLog widget.

        Parameters
        ----------
        line : str
            The line of text to write to the terminal log.

        """
        log = self.query_one("#pytest_log", RichLog)
        log.write(line)
