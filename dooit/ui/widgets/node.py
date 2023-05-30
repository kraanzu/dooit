from typing import Iterator, List, Literal, Optional, Type, Union
from textual.app import ComposeResult
from textual.widget import Widget
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from dooit.ui.widgets.simple_input import SimpleInput
from .utils import Pointer


class Node(Widget):
    pointer = ">"
    _expand = False
    ModelType: Type[Workspace | Todo] = Workspace

    def __init__(self, model: ModelType, display: bool = True):
        self.model = model
        self.force_display = display
        super().__init__(id=self.model.uuid)

    @property
    def expanded(self):
        return self._expand

    def _get_model_children(self) -> List[ModelType]:
        raise NotImplementedError

    def _get_all_children(self):
        return self.query(self.__class__)

    def _is_editing(self) -> Union[Literal[False], SimpleInput]:
        if q := self.query(".editing"):
            q = q.first()
            if isinstance(q, SimpleInput):
                return q

        return False

    def highlight(self, on: bool = True):
        pointer = self.query("Pointer").first()
        if isinstance(pointer, Pointer):
            pointer.show() if on else pointer.hide()

        if on:
            for i in self.query(SimpleInput):
                i.remove_class("dim")
                i.add_class("highlight")
        else:
            for i in self.query(SimpleInput):
                i.add_class("dim")
                i.remove_class("highlight")

    def start_edit(self, property: str):
        self.query_one(f"#{self.id}-{property}", expect_type=SimpleInput).start_edit()
        self.refresh()

    def stop_edit(self):
        if widget := self._is_editing():
            widget.stop_edit()

    def draw(self) -> Iterator[Widget]:
        raise NotImplementedError

    def compose(self) -> ComposeResult:
        if not self.force_display and self.model.nest_level:
            self.display = False

        for widget in self.draw():
            yield widget

        for child in self._get_model_children():
            yield self.__class__(child, display=False)

    async def force_refresh(self):
        children = self._get_model_children()
        for i in children:
            if query := self.query(f"#{i.uuid}"):
                await self.mount(query.first())
            else:
                child = self.__class__(i, display=False)
                await self.mount(child)

    # ------------------------------------------

    def show_children(self):
        for i in self._get_all_children():
            self.query_one(f"#{i.id}").display = True

    def hide_children(self):
        for i in self._get_all_children():
            self.query_one(f"#{i.id}").display = False

    def toggle_expand(self):
        self._expand = not self._expand
        if self._expand:
            self.show_children()
        else:
            self.hide_children()

    def toggle_expand_parent(self) -> Optional[str]:
        if self.model.has_same_parent_kind:
            return self.model.parent.uuid

    async def refresh_value(self):
        for i in self.query(SimpleInput):
            i.refresh_value()

    async def keypress(self, key: str):
        if w := self._is_editing():
            await w.keypress(key)
