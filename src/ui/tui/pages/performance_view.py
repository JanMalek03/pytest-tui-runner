from textual.containers import Vertical, ScrollableContainer
from textual.widgets import Label


class PerformanceView(Vertical):

    def __init__(self):
        super().__init__()
        self.output = ScrollableContainer(Label("Here will be the performance of the tests."))

    def compose(self):
        yield self.output
