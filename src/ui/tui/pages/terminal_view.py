from textual.containers import Vertical, ScrollableContainer
from textual.widgets import Label


class TerminalView(Vertical):

    def __init__(self):
        super().__init__()
        self.output = ScrollableContainer(Label("Zde bude výstup pytestu"))

    def compose(self):
        yield self.output

    def update_output(self, text: str):
        self.output.update(Label(text))
