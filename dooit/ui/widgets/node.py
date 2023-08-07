from typing import Iterator, List, Literal, Optional, Type, Union
import pyperclip
from textual.app import ComposeResult
from textual.widget import Widget
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from dooit.ui.events.events import ChangeStatus
from dooit.ui.widgets.inputs import Description
from dooit.ui.widgets.simple_input import SimpleInput
from .utils import Pointer


class Node(Widget):
    pointer_icon = ">"
    _expand = False
    ModelType: Type[Union[Workspace, Todo]]

    def __init__(self, model, force_display: bool = True):
        super().__init__(id=model.uuid)

        self.model = model
        self.force_display = force_display
        self.pointer = Pointer(self.pointer_icon)
        self.setup_children()

    def setup_children(self) -> None:
        pass

    def get_child_inputs(self) -> List[SimpleInput]:
        return []

    @property
    def expanded(self):
        return self._expand

    def _get_model_children(self) -> List[Union[Workspace, Todo]]:
        raise NotImplementedError

    def _get_all_children(self):
        return [i for i in self.children if isinstance(i, self.__class__)]

    def _is_editing(self) -> Union[Literal[False], SimpleInput]:
        if q := self.query(".editing"):
            q = q.first()
            if isinstance(q, SimpleInput):
                return q

        return False

    def highlight(self, on: bool = True):
        if on:
            self.pointer.show()
            for i in self.get_child_inputs():
                i.remove_class("dim")
                i.add_class("highlight")
        else:
            self.pointer.hide()
            for i in self.get_child_inputs():
                i.add_class("dim")
                i.remove_class("highlight")

        self.scroll_visible()

    def start_edit(self, property: str):
        if property == "due":
            self.post_message(ChangeStatus("DATE"))
        else:
            self.post_message(ChangeStatus("INSERT"))

        self.query_one(f"#{self.id}-{property}", expect_type=SimpleInput).start_edit()
        self.refresh()

    def draw(self) -> Iterator[Widget]:
        raise NotImplementedError

    def compose(self) -> ComposeResult:
        if not self.force_display and self.model.nest_level:
            self.display = False

        for widget in self.draw():
            yield widget

        for child in self._get_model_children():
            yield self.__class__(child, force_display=False)

    async def force_refresh(self):
        children = self._get_model_children()
        for i in children:
            if query := self.query(f"#{i.uuid}"):
                await self.mount(query.first())
            else:
                child = self.__class__(i, force_display=False)
                await self.mount(child)

    # ------------------------------------------

    def show_children(self):
        for i in self._get_all_children():
            i.display = True

    def hide_children(self):
        for i in self._get_all_children():
            i.display = False

    def toggle_expand(self):
        self._expand = not self._expand
        if self._expand:
            self.show_children()
        else:
            self.hide_children()

    def toggle_expand_parent(self) -> Optional[str]:
        if self.model.has_same_parent_kind:
            return self.model.parent.uuid

    async def refresh_value(self, input_type: Optional[Type] = None):
        input_type = input_type or SimpleInput
        for i in self.query(input_type):
            i.refresh_value()

    async def keypress(self, key: str):
        if w := self._is_editing():
            await w.keypress(key)

    async def apply_filter(self, filter: str) -> None:
        widget = self.query_one(
            f"#{self.model.uuid}-description", expect_type=Description
        )
        widget.apply_filter(filter)

    async def copy_text(self):
        widget = self.query_one(
            f"#{self.model.uuid}-description", expect_type=Description
        )
        pyperclip.copy(widget.value)
