from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, TabbedContent, TabPane, Button, Label

from src.ui.tui.pages.terminal_view import TerminalView
from src.ui.tui.pages.tests_view import TestsView
from src.ui.tui.pages.performance_view import PerformanceView


class TestRunnerApp(App):
    CSS_PATH = "styles/tests_view.css"
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with TabbedContent():
            with TabPane("Tests"):
                yield TestsView()
            with TabPane("Terminal"):
                yield TerminalView()
            with TabPane("Performance"):
                yield PerformanceView()


if __name__ == "__main__":
    TestRunnerApp().run()
