from typing import Optional, Type
from rich.align import Align
from rich.box import HEAVY
from rich.console import RenderableType
from rich.tree import Tree
from rich.panel import Panel
from rich.text import Text
from rich.style import StyleType
from textual.widget import Widget
from dooit.ui.events import ApplySortMethod, ChangeStatus, Notify
from dooit.utils import KeyBinder


class SortOptions(Widget):
    """
    A list class to show and select the items in a list
    """

    key_manager = KeyBinder()

    def __init__(
        self,
        name: str | None = None,
        options: list[str] = [],
        parent_widget: Optional[Widget] = None,
        style_unfocused: StyleType = "white",
        style_focused: StyleType = "bold reverse green ",
        pad: bool = True,
        wrap: bool = True,
    ) -> None:
        super().__init__(name=name)
        self.options = options
        self.style_unfocused = style_unfocused
        self.style_focused = style_focused
        self.pad = pad
        self.wrap = wrap
        self.parent_widget = parent_widget
        self.highlighted = 0

    def highlight(self, id: int) -> None:
        self.highlighted = id
        self.refresh(layout=True)

    def hide(self) -> None:
        self.visible = False

    async def move_down(self) -> None:
        """
        Moves the highlight down
        """

        self.highlight(min(self.highlighted + 1, len(self.options) - 1))

    async def move_up(self) -> None:
        """
        Moves the highlight up
        """

        self.highlight(max(self.highlighted - 1, 0))

    async def move_to_top(self) -> None:
        """
        Moves the cursor to the top
        """
        self.highlight(0)

    async def move_to_bottom(self) -> None:
        """
        Moves the cursor to the bottom
        """

        self.highlight(len(self.options) - 1)

    async def sort_menu_toggle(self):
        await self.send_message(ChangeStatus, "NORMAL")
        self.visible = False

    async def send_message(self, event: Type, *args):
        if self.parent_widget:
            await self.parent_widget.post_message(
                event(
                    self.parent_widget,
                    *args,
                )
            )

    async def handle_key(self, key: str) -> None:

        if key == "escape":
            await self.sort_menu_toggle()
            return

        if key == "enter":
            await self.send_message(ApplySortMethod, self.options[self.highlighted])
            await self.sort_menu_toggle()
            return

        self.key_manager.attach_key(key)
        bind = self.key_manager.get_method()
        if bind:
            if hasattr(self, bind.func_name):
                func = getattr(self, bind.func_name)
                await func(*bind.params)
            else:
                await self.post_message(
                    Notify(self, "[yellow]No such operation for sort menu![/yellow]")
                )

        self.refresh()

    def add_option(self, option: str) -> None:
        self.options.append(option)
        self.refresh()

    def render(self) -> RenderableType:

        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True

        for index, option in enumerate(self.options):
            label = Text(option)
            label = Text("  ") + label

            label.pad_right(self.size.width)
            label.plain = label.plain.ljust(20)
            if index != self.highlighted:
                label.stylize(self.style_unfocused)
            else:
                label.stylize(self.style_focused)

            meta = {
                "selected": index,
            }
            label.apply_meta(meta)
            tree.add(label)

        return self.render_panel(tree)

    def render_panel(self, tree) -> RenderableType:
        return Align.center(
            Panel.fit(
                tree,
                title="Sort",
                width=20,
                box=HEAVY,
            ),
            vertical="middle",
            height=self._size.height,
        )
