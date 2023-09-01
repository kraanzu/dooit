from typing_extensions import Self
from typing import Iterator, List, Literal, Optional, Type, Union
import pyperclip
from rich.console import RenderableType
from textual.app import ComposeResult
from textual.widget import Widget
from dooit.api.model import Ok, Result, Warn
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from dooit.ui.events.events import ChangeStatus, DateModeSwitch
from dooit.ui.widgets.inputs import Description
from dooit.ui.widgets.simple_input import SimpleInput
from .utils import Pointer


class Node(Widget):
    """
    Base Widget to represent a Model class
    """

    pointer_icon = ">"
    _expand = False
    ModelType: Type[Union[Workspace, Todo]]

    def __init__(self, model, force_display: bool = True):
        super().__init__(id=model.uuid)

        self.model = model
        self.force_display = force_display
        self.pointer = Pointer(self.pointer_icon)
        self.setup_children()

    @property
    def expanded(self) -> bool:
        return self._expand

    def setup_children(self) -> None:
        pass

    def _get_model_children(self) -> List[Union[Workspace, Todo]]:
        raise NotImplementedError

    def _get_all_children(self) -> List[Self]:
        return [i for i in self.children if isinstance(i, self.__class__)]

    def _is_editing(self) -> Union[Literal[False], SimpleInput]:
        if q := self.query(".editing"):
            q = q.first()
            if isinstance(q, SimpleInput):
                return q

        return False

    def highlight(self, on: bool = True) -> None:
        if on:
            self.pointer.show()
            self.add_class("highlight")
        else:
            self.pointer.hide()
            self.remove_class("highlight")

        self.scroll_visible()

    def unflash(self) -> None:
        self.remove_class("yank")

    def flash(self) -> None:
        """
        Function to flash the node when yanked
        """

        self.add_class("yank")
        self.set_timer(0.5, self.unflash)

    def start_edit(self, property: str) -> Result:
        self.add_class("editing")
        if not hasattr(self.model, property):
            return Warn(f"{self.model.__class__.__name__} has no property `{property}`")

        if property == "due":
            style = getattr(self.screen, "date_style")
            if style != "classic":
                self.post_message(DateModeSwitch())

            self.post_message(ChangeStatus("DATE"))
        else:
            self.post_message(ChangeStatus("INSERT"))

        self.query_one(f"#{self.id}-{property}", expect_type=SimpleInput).start_edit()
        self.refresh()
        return Ok()

    def draw(self) -> Iterator[Widget]:
        raise NotImplementedError

    def compose(self) -> ComposeResult:
        if not self.force_display and self.model.nest_level:
            self.display = False

        for widget in self.draw():
            yield widget

        for child in self._get_model_children():
            yield self.__class__(child, force_display=False)

    # ------------------------------------------

    @property
    def is_visible(self) -> bool:
        parent = self
        while isinstance(parent, self.__class__):
            if not parent:
                break

            if not parent.display:
                return False

            parent = parent.parent

        return True

    def show_children(self) -> None:
        for i in self._get_all_children():
            i.display = True

    def hide_children(self) -> None:
        for i in self._get_all_children():
            i.display = False

    def toggle_expand(self) -> None:
        self._expand = not self._expand
        if self._expand:
            self.show_children()
        else:
            self.hide_children()

    def toggle_expand_parent(self) -> Optional[str]:
        if self.model.has_same_parent_kind:
            return self.model.parent.uuid

    async def refresh_value(self, input_type: Optional[Type] = None) -> None:
        input_type = input_type or SimpleInput
        for i in self.query(input_type):
            i.refresh_value()

    async def keypress(self, key: str) -> None:
        if w := self._is_editing():
            await w.keypress(key)

    async def apply_filter(self, filter: str) -> None:
        widget = self.query_one(
            f"#{self.model.uuid}-description", expect_type=Description
        )
        widget.apply_filter(filter)

    async def copy_text(self) -> None:
        widget = self.query_one(
            f"#{self.model.uuid}-description", expect_type=Description
        )
        pyperclip.copy(widget.value)

    def render(self) -> RenderableType:
        return ""
