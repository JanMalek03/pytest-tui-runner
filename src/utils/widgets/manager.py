from src.utils.widgets.factory import generate_widgets_from_config
from src.utils.widgets.serializer import load_widget_state, save_widget_state
from src.utils.widgets.composer import compose_widgets
from logs.logger_config import logger
from src.config.paths import STATE_PATH

class WidgetManager:
    def __init__(self, config: dict, state_path: str = STATE_PATH):
        self.config = config
        self.state_path = state_path
        self.widgets = {}

        logger.debug("Initializing WidgetManager...")
        self.generate()
        # self.load_state()
        logger.info("WidgetManager initialized.")

    def generate(self):
        """Generates widgets from the provided configuration.
        It will generate widgets based on the user configuration and also according to the saved state of the widgets."""

        try:
            self.widgets = generate_widgets_from_config(self.config, self.state_path)
            if not self.widgets:
                logger.warning("No widgets generated from the configuration.")
        except Exception as e:
            logger.error(f"Error generating widgets: {e}", exc_info=True)

    def load_state(self):
        try:
            load_widget_state(self.widgets, self.state_path)
        except FileNotFoundError:
            logger.warning(f"Soubor se stavem widgetů '{self.state_path}' nenalezen")
        except Exception as e:
            logger.error(f"Error loading widget state: {e}", exc_info=True)

    def save_state(self):
        try:
            save_widget_state(self.widgets, self.state_path)
        except Exception as e:
            logger.error(f"Error saving widget state: {e}", exc_info=True)

    def compose(self):
        return compose_widgets(self.widgets)

    def get_widgets(self):
        return self.widgets
