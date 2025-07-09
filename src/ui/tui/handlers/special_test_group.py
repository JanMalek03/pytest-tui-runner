from textual.widget import Widget
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Input, Select

class SpecialTestGroup(Vertical):
    def __init__(self, test_name: str, widget_list: list[Widget]):
        super().__init__(classes="special_test_class")
        self.test_name = test_name
        self.widget_template = widget_list.copy()
        self.widget_list = widget_list
        self.rows: list[Horizontal] = []
        self.instance_counter = 0

    async def on_mount(self):
        self._clean_old_widget_list()
        await self.add_instance()

    def _clean_old_widget_list(self):
        self.widget_list.clear()

    def _update_widget_list(self, widgets: list[Widget]):
        self.widget_list.extend(widgets)

    async def add_instance(self):
        widgets = self._clone_widgets()
        self._update_widget_list(widgets)
        row_id = f"{self.test_name.replace(' ', '_')}_{self.instance_counter}"
        self.instance_counter += 1

        row = Horizontal(*widgets, classes="special_test_row", id=f"row_{row_id}")
        self.rows.append(row)
        await self.mount(row)
        await self._refresh_buttons()

    async def _refresh_buttons(self):
        for row in self.rows:
            for child in row.children:
                if isinstance(child, Button):
                    await child.remove()

        for i, row in enumerate(self.rows):
            if i == len(self.rows) - 1:
                add_button = Button("+", variant="success", id=f"add_button_{row.id}")
                await row.mount(add_button, before=row.children[0] if row.children else None)
            else:
                delete_button = Button("-", variant="error", id=f"delete_button_{row.id}")
                await row.mount(delete_button, before=row.children[0] if row.children else None)

    def _clone_widgets(self) -> list[Widget]:
        cloned = []
        for widget in self.widget_template:
            if isinstance(widget, Input):
                cloned.append(Input(placeholder=widget.placeholder, name=widget.name))
            elif isinstance(widget, Select):
                cloned.append(Select.from_values(sorted(widget._legal_values), name=widget.name, allow_blank=widget._allow_blank, value=widget.value))
        return cloned

    async def on_button_pressed(self, event):
        btn_id = event.button.id
        if not btn_id:
            return

        if btn_id.startswith("add_button_"):
            await self.add_instance()

        elif btn_id.startswith("delete_button_"):
            row_id = btn_id.replace("delete_button_", "")
            row_to_delete = self.query_one(f"#{row_id}", Horizontal)
            if row_to_delete in self.rows:
                self.rows.remove(row_to_delete)
                await row_to_delete.remove()
                await self._refresh_buttons()
