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
from dooit.ui.registry import registry


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

    def _draw_table(self) -> Table:
        table = registry.get_todo_table(self.model.parent)
        layout = registry.get_todo_layout()

        row = []
        for column, formatter in layout:
            value = getattr(self, f"_draw_{column.value}")()
            if self.editing != column.value:
                value = formatter(value, self._model)

            row.append(value)

        table.add_row(*row)

        return table

    def make_renderable(self) -> RenderableType:
        return self._draw_table()

    def edit(self, param: str):
        pass
