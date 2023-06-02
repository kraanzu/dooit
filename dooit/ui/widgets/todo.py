from typing import Iterator, List
from textual.widget import Widget
from dooit.api.todo import Todo
from dooit.ui.widgets.inputs import (
    Description,
    Due,
    Effort,
    Recurrence,
    Status,
    Tags,
    Urgency,
)
from dooit.ui.widgets.utils import Padding, Pointer
from .node import Node


class ExpandedHorizontal(Widget):
    DEFAULT_CSS = """
    ExpandedHorizontal {
        layout: horizontal;
        height: auto;
    }
    """

    def on_mount(self) -> None:
        self.styles.width = "1fr"


class TodoWidget(Node):
    ModelType = Todo

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
        await self.refresh_value()

    def draw(self) -> Iterator[Widget]:
        with ExpandedHorizontal():
            yield Pointer(self.pointer)
            yield Padding(self.model.nest_level)

            with ExpandedHorizontal():
                yield Status(model=self.model)
                yield Description(model=self.model)
                yield Effort(model=self.model)
                yield Recurrence(model=self.model)
                yield Tags(model=self.model)

            yield Due(model=self.model)
            yield Urgency(model=self.model)
