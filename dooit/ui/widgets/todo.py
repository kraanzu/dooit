from typing import Iterator, List
from textual.containers import Horizontal
from textual.widget import Widget
from dooit.api.todo import Todo
from dooit.ui.widgets.inputs import (
    Description,
    Due,
    Effort,
    Recurrence,
    Status,
    Urgency,
)
from dooit.ui.widgets.utils import Padding
from dooit.utils.conf_reader import config_man
from .node import Node

EDITING = config_man.get("TODO").get("editing")
POINTER_ICON = config_man.get("TODO").get("pointer")


class TodoGrid(Widget):
    DEFAULT_CSS = f"""
    TodoGrid {{
        layout: grid;
        grid-size: 5;
        grid-columns: auto auto 1fr auto auto;
        height: auto;
    }}

    TodoGrid > Horizontal > Description.editing {{
        color: {EDITING};
    }}
    """


class TodoWidget(Node):
    ModelType = Todo
    pointer_icon = POINTER_ICON

    def setup_children(self):
        self.status = Status(model=self.model)
        self.description = Description(model=self.model)
        self.effort = Effort(model=self.model)
        self.recurrence = Recurrence(model=self.model)
        self.due = Due(model=self.model)
        self.urgency = Urgency(model=self.model)

    def _get_model_children(self) -> List[ModelType]:
        return self.model.todos

    async def increase_urgency(self):
        self.model.increase_urgency()
        await self.refresh_value()

    async def decrease_urgency(self):
        self.model.decrease_urgency()
        await self.refresh_value()

    async def toggle_complete(self):
        self.model.toggle_complete()

        parent = self.parent
        while parent:
            if not isinstance(parent, TodoWidget):
                break

            await parent.refresh_value()
            parent = parent.parent

        await self.refresh_value()

    def draw(self) -> Iterator[Widget]:
        with TodoGrid():
            yield self.pointer
            yield Padding(self.model.nest_level)

            with Horizontal():
                yield self.status
                yield self.description
                yield self.effort
                yield self.recurrence

            yield self.due
            yield self.urgency
