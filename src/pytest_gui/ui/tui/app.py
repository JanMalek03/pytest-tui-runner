from textual.app import App, ComposeResult
from textual.widgets import TabbedContent, TabPane

from pytest_gui.ui.tui.pages.performance_view import PerformanceView
from pytest_gui.ui.tui.pages.terminal_view import TerminalView
from pytest_gui.ui.tui.pages.tests_view import TestsView


class TestRunnerApp(App):
    """Main application class for the pytest-gui TUI.

    Handles the layout and navigation between Tests, Terminal, and Performance views.
    """

    CSS_PATH = "styles/tests_view.css"

    def compose(self) -> ComposeResult:
        """Compose the main layout with tabbed views for Tests, Terminal, and Performance."""
        # Uncomment this if you want to have Header on the page
        # yield Header()

        with TabbedContent():
            with TabPane("Tests"):
                yield TestsView()
            with TabPane("Terminal"):
                self.terminal_view = TerminalView()
                yield self.terminal_view
            with TabPane("Performance"):
                yield PerformanceView()

        # Uncomment this if you want to have Footer on the page
        # yield Footer()


if __name__ == "__main__":
    TestRunnerApp().run()
