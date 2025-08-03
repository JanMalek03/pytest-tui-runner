from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane

from src.ui.tui.pages.performance_view import PerformanceView
from src.ui.tui.pages.terminal_view import TerminalView
from src.ui.tui.pages.tests_view import TestsView


class TestRunnerApp(App):
    CSS_PATH = "styles/tests_view.css"

    def compose(self) -> ComposeResult:
        # yield Header()

        with TabbedContent():
            with TabPane("Tests"):
                yield TestsView()
            with TabPane("Terminal"):
                self.terminal_view = TerminalView()
                yield self.terminal_view
            with TabPane("Performance"):
                yield PerformanceView()

        # yield Footer()


if __name__ == "__main__":
    TestRunnerApp().run()
