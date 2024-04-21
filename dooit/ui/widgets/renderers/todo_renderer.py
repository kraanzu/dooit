from typing import Dict, List, Text
from rich.console import RenderableType
from rich.table import Table
from .base_renderer import BaseRenderer, Todo


class TodoRender(BaseRenderer):
    @property
    def model(self) -> Todo:
        if not isinstance(self._model, Todo):
            raise ValueError(f"Expected Todo, got {type(self._model)}")
        return self._model

    def _draw_status(self, todo: Todo) -> Text:
        return todo.status

    def _draw_description(self, todo: Todo) -> Text:
        return todo.description

    def _draw_due(self, todo: Todo) -> Text:
        return todo.due

    def _draw_urgency(self, todo: Todo) -> Text:
        return todo.urgency

    def _draw_effort(self, todo: Todo) -> Text:
        return todo.effort

    def _draw_recurrence(self, todo: Todo) -> Text:
        return todo.recurrence

    def _draw_table(self, config: Dict[str, List]) -> Table:
        table = Table.grid(expand=True)
        table.add_column("status")
        table.add_column("description", ratio=1)
        table.add_column("due")
        table.add_column("urgency")

        t = self.model
        table.add_row(*[t.status, t.description, t.due, t.urgency])
        return table

    def get_table_config(self) -> Dict[str, List]:
        return {}

    @property
    def prompt(self) -> RenderableType:
        config = self.get_table_config()
        return self._draw_table(config)

    def edit(self, param: str):
        pass
