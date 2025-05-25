from src.utils.widgets.factory import generate_widgets_from_config
from src.utils.widgets.serializer import load_widget_state, save_widget_state
from src.utils.widgets.composer import compose_widgets
from logs.logger_config import logger

class WidgetManager:
    def __init__(self, config: dict, state_path: str = "data/widgets_state.json"):
        self.config = config
        self.state_path = state_path
        self.widgets = {}

        logger.debug("Initializing WidgetManager...")
        self.generate()
        self.load_state()
        logger.info("WidgetManager initialized.")

    def generate(self):
        try:
            self.widgets = generate_widgets_from_config(self.config)
        except Exception as e:
            logger.error(f"Error generating widgets: {e}", exc_info=True)

    def load_state(self):
        try:
            load_widget_state(self.widgets, self.state_path)
        except FileNotFoundError:
            logger.warning(f"Soubor se stavem widgetů '{self.state_path}' nenalezen")
        except Exception as e:
            logger.error(f"Chyba při načítání stavu widgetů: {e}", exc_info=True)

    def save_state(self):
        try:
            save_widget_state(self.widgets, self.state_path)
        except Exception as e:
            logger.error(f"Error saving widget state: {e}", exc_info=True)

    def compose(self):
        return compose_widgets(self.widgets)

    def get_widgets(self):
        return self.widgets
