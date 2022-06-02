from rich.align import Align
from rich.box import MINIMAL
from rich.console import RenderableType
from rich.tree import Tree
from rich.panel import Panel
from rich.text import Text
from rich.style import StyleType
from textual.widget import Widget
from textual import events

from doit.ui.events.events import ApplySortMethod


class SortOptions(Widget):
    """
    A list class to show and select the items in a list
    """

    def __init__(
        self,
        name: str | None = None,
        options: list[str] = [],
        style_unfocused: StyleType = "",
        style_focused: StyleType = "bold green",
        pad: bool = True,
        rotate: bool = False,
        wrap: bool = True,
        panel: Panel = Panel(""),
    ) -> None:
        super().__init__(name)
        self.options = options
        self.style_unfocused = style_unfocused
        self.style_focused = style_focused
        self.pad = pad
        self.panel = panel
        self.rotate = rotate
        self.wrap = wrap
        self.highlighted = 0

    def highlight(self, id: int) -> None:
        self.highlighted = id
        self.refresh(layout=True)

    def move_cursor_down(self) -> None:
        """
        Moves the highlight down
        """

        if self.rotate:
            self.highlight((self.highlighted + 1) % len(self.options))
        else:
            self.highlight(min(self.highlighted + 1, len(self.options) - 1))

    def move_cursor_up(self):
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

    async def key_press(self, event: events.Key) -> None:
        event.stop()

        match event.key:
            case "escape":
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
                await self.emit(ApplySortMethod(self, self.options[self.highlighted]))

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        """
        Move the highlight along with mouse hover
        """
        self.highlight(event.style.meta.get("selected"))

    def add_option(self, option: str) -> None:
        self.options.append(option)
        self.refresh()

    def render(self) -> RenderableType:

        # 1 borders + 1 space padding on each side
        width = self.size.width - 4

        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True

        for index, option in enumerate(self.options):
            if isinstance(option, str):
                option = Text(option)

            option.pad_right(width - len(option) - 1)
            option = Text(" ") + option

            if self.wrap:
                option.plain = option.plain[:width]

            if index != self.highlighted:
                option.stylize(self.style_unfocused)
            else:
                option.stylize(self.style_focused)

            meta = {
                "@click": f"click_label({index})",
                "selected": index,
            }
            option.apply_meta(meta)
            tree.add(option)

        return self.render_panel(tree)

    def render_panel(self, tree):
        return Panel(
            Align.center(
                Panel.fit(tree, width=15),
                vertical="middle",
            ),
            box=MINIMAL,
        )

    async def action_click_label(self, id):
        self.highlight(id)
        await self.emit(ApplySortMethod(self, self.options[self.highlighted]))
