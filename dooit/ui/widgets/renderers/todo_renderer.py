from typing import Dict, List
from rich.text import TextType
from rich.console import RenderableType
from rich.table import Table

from dooit.ui.widgets.inputs.inputs import (
    Due,
    Effort,
    Recurrence,
    Status,
    TodoDescription,
    Urgency,
)
from .base_renderer import BaseRenderer, Todo


class TodoRender(BaseRenderer):
    @property
    def model(self) -> Todo:
        if not isinstance(self._model, Todo):
            raise ValueError(f"Expected Todo, got {type(self._model)}")
        return self._model

    def post_init(self):
        self.description = TodoDescription(self.model)
        self.due = Due(self.model)
        self.status = Status(self.model)
        self.urgency = Urgency(self.model)
        self.effort = Effort(self.model)
        self.recurrence = Recurrence(self.model)
        self.refresh_prompt()

    def _draw_status(self) -> TextType:
        return self.status.render()

    def _draw_description(self) -> TextType:
        return self.description.render()

    def _draw_due(self) -> TextType:
        return self.due.render()

    def _draw_urgency(self) -> TextType:
        return self.urgency.render()

    def _draw_effort(self) -> TextType:
        return self.effort.render()

    def _draw_recurrence(self) -> TextType:
        return self.recurrence.render()

    def _draw_table(self, config: Dict[str, List]) -> Table:
        table = Table.grid(expand=True)
        table.add_column("status")
        table.add_column("description", ratio=1)
        table.add_column("due")
        table.add_column("urgency")

        table.add_row(
            *[
                self._draw_status(),
                self._draw_description(),
                self._draw_due(),
                self._draw_urgency(),
            ]
        )
        return table

    def get_table_config(self) -> Dict[str, List]:
        return {}

    def make_renderable(self) -> RenderableType:
        config = self.get_table_config()
        return self._draw_table(config)

    def edit(self, param: str):
        pass
