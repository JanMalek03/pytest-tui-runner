from textual.widget import Widget
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Label, Input, Select

class SpecialTestGroup(Vertical):
    def __init__(self, test_name: str, widget_template: list[Widget]):
        super().__init__()
        self.test_name = test_name
        self.widget_template = widget_template
        self.instance_counter = 0

    async def on_mount(self):
        await self.add_instance()

    async def add_instance(self):
        widgets = self._clone_widgets()
        add_button = Button("+", variant="primary", id=f"add_button_{self.test_name.replace(" ", "_")}_{self.instance_counter}")
        self.instance_counter += 1

        row = Horizontal(
            add_button,
            *widgets,
            classes="special_test_row"
        )
        await self.mount(row)

    def _clone_widgets(self) -> list[Widget]:
        cloned = []
        for widget in self.widget_template:
            if isinstance(widget, Input):
                cloned.append(Input(placeholder=widget.placeholder, name=widget.name))
            elif isinstance(widget, Select):
                cloned.append(Select.from_values(widget._legal_values, name=widget.name, allow_blank=widget._allow_blank, value=widget.value))
        return cloned

    async def on_button_pressed(self, event):
        if event.button.id and event.button.id.startswith(f"add_button_{self.test_name.replace(" ", "_")}"):
            await self.add_instance()
