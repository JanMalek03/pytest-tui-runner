from textual.containers import Vertical
from textual.widgets import RichLog


class TerminalView(Vertical):
    def compose(self):
        yield RichLog(id="pytest_log", highlight=True, wrap=True)

    def write_line(self, line: str):
        log = self.query_one("#pytest_log", RichLog)
        log.write(line)
