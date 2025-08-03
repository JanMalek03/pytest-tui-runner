from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button, Input, Select


class SpecialTestGroup(Vertical):
    def __init__(self, initial_rows: list[list[Widget]]):
        super().__init__(classes="special_test_class")
        self.row_template = self._clone_widgets(initial_rows[0]) if initial_rows else []
        self.original_input = initial_rows
        self.rows: list[Horizontal] = []

    async def on_mount(self) -> None:
        for widget_row in self.original_input:
            await self._add_row(widget_row, update_rows=False)
        await self._refresh_buttons()

    async def _add_row(self, to_clone: list[Widget] | None = None, update_rows=True) -> None:
        widgets = self._clone_widgets(to_clone)

        row = Horizontal(classes="special_test_row")
        self.rows.append(row)
        await self.mount(row)

        for widget in widgets:
            await row.mount(widget)

        if update_rows:
            self._update_initial_rows()

    def _clone_widgets(self, widgets: list[Widget]) -> list[Widget]:
        cloned = []
        for widget in widgets:
            if isinstance(widget, Input):
                cloned.append(Input(value=widget.value, name=widget.name, placeholder=widget.placeholder))
            elif isinstance(widget, Select):
                cloned.append(
                    Select.from_values(
                        values=sorted(widget._legal_values),
                        name=widget.name,
                        allow_blank=widget._allow_blank,
                        value=widget.value,
                    ),
                )
        return cloned

    async def _remove_row(self, row: Horizontal) -> None:
        if row in self.rows:
            self.rows.remove(row)
            await row.remove()
            self._update_initial_rows()
            await self._refresh_buttons()

    # TODO: co se stane, kdyz bude vice specialTestGroup? Potom budou kolidovat id ne? Asi potreba zahrnout test name do id
    async def _refresh_buttons(self) -> None:
        for row in self.rows:
            if row.children and isinstance(row.children[0], Button):
                await row.children[0].remove()

        for i, row in enumerate(self.rows):
            if i == len(self.rows) - 1:
                button = Button("+", id=f"add_{i}", variant="success")
            else:
                button = Button("-", id=f"remove_{i}", variant="error")

            await row.mount(button, before=row.children[0] if row.children else None)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        btn_id = event.button.id
        if not btn_id:
            return

        if btn_id.startswith("add_"):
            await self._add_row(self.row_template)
            await self._refresh_buttons()

        elif btn_id.startswith("remove_"):
            index = int(btn_id.replace("remove_", ""))
            if 0 <= index < len(self.rows):
                await self._remove_row(self.rows[index])

    def _update_initial_rows(self) -> None:
        self.original_input.clear()

        for row in self.rows:
            widgets = []
            for widget in row.children:
                if isinstance(widget, (Input, Select)):
                    widgets.append(widget)
            self.original_input.append(widgets)
