from collections.abc import Iterator

from textual.containers import ScrollableContainer, Vertical
from textual.widget import Widget
from textual.widgets import Label


class PerformanceView(Vertical):
    """A view that displays the performance of the tests in a scrollable container."""

    def __init__(self) -> None:
        """Initialize the PerformanceView with a scrollable container for test performance output."""
        super().__init__()
        self.output = ScrollableContainer(Label("Here will be the performance of the tests."))

    def compose(self) -> Iterator[Widget]:
        """Compose the widgets for the performance view.

        Yields
        ------
        Widget
            The scrollable container displaying test performance.

        """
        yield self.output
