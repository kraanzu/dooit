from os import get_terminal_size
from typing import Optional
from rich.align import Align
from rich.box import HEAVY
from rich.console import RenderableType
from rich.tree import Tree
from rich.panel import Panel
from rich.text import Text
from rich.style import StyleType
from textual.widget import Widget
from textual import events

from ...ui.events.events import ApplySortMethod, ChangeStatus


class SortOptions(Widget):
    """
    A list class to show and select the items in a list
    """

    def __init__(
        self,
        name: str | None = None,
        options: list[str] = [],
        parent_widget: Optional[Widget] = None,
        style_unfocused: StyleType = "white",
        style_focused: StyleType = "bold reverse green ",
        pad: bool = True,
        rotate: bool = False,
        wrap: bool = True,
    ) -> None:
        super().__init__(name)
        self.options = options
        self.style_unfocused = style_unfocused
        self.style_focused = style_focused
        self.pad = pad
        self.rotate = rotate
        self.wrap = wrap
        self.parent_widget = parent_widget
        self.highlighted = 0

    def highlight(self, id: int) -> None:
        self.highlighted = id
        self.refresh(layout=True)

    async def hide(self):
        await self.handle_key(events.Key(self, "escape"))

    def move_cursor_down(self) -> None:
        """
        Moves the highlight down
        """

        if self.rotate:
            self.highlight((self.highlighted + 1) % len(self.options))
        else:
            self.highlight(min(self.highlighted + 1, len(self.options) - 1))

    def move_cursor_up(self) -> None:
        """
        Moves the highlight up
        """

        if self.rotate:
            self.highlight(
                (self.highlighted - 1 + len(self.options)) % len(self.options)
            )
        else:
            self.highlight(max(self.highlighted - 1, 0))

    def move_cursor_to_top(self) -> None:
        """
        Moves the cursor to the top
        """
        self.highlight(0)

    def move_cursor_to_bottom(self) -> None:
        """
        Moves the cursor to the bottom
        """

        self.highlight(len(self.options) - 1)

    async def handle_key(self, event: events.Key) -> None:
        event.stop()

        match event.key:
            case "escape":
                await self.post_message(ChangeStatus(self, "NORMAL"))
                self.visible = False
            case "j" | "down":
                self.move_cursor_down()
            case "k" | "up":
                self.move_cursor_up()
            case "g" | "home":
                self.move_cursor_to_top()
            case "G" | "end":
                self.move_cursor_to_bottom()
            case "enter":
                if self.parent_widget:
                    await self.parent_widget.emit(
                        ApplySortMethod(
                            self.parent_widget,
                            self.options[self.highlighted],
                        )
                    )
                await self.hide()
            case "s":
                await self.hide()

        self.refresh()

    def add_option(self, option: str) -> None:
        self.options.append(option)
        self.refresh()

    def render(self) -> RenderableType:

        # 1 borders + 1 space padding on each side
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True

        for index, option in enumerate(self.options):
            label = Text(option)
            match option:
                case "about":
                    label = Text("    ") + label
                case "due":
                    label = Text("    ") + label
                case "status":
                    label = Text("    ") + label
                case "urgency":
                    label = Text("    ") + label
                case _:
                    label = Text(" X   ") + label

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
                # box=HEAVY,
            ),
            vertical="middle",
            height=self._size.height,
        )
