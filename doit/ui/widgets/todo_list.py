import re
from os import get_terminal_size
from datetime import datetime
from typing import Callable
import pyperclip
from rich.align import Align
from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode, NodeID

from doit.ui.widgets.simple_input import View

from ...ui.widgets import NestedListEdit
from ...ui.widgets.entry import Entry
from ...ui.events import *  # NOQA

NodeDataTye = Entry

EMPTY_TODO = """
              [b blue][/b blue]
        [d white]Wow! so empty?
You can add todo by pressing '[b green]a[/b green]'[/d white]
"""


def percentage(percent, total) -> int:
    return round(percent * total / 100)


class TodoList(NestedListEdit):
    """
    A Class that allows editing while displaying trees
    """

    def __init__(self, name: str | None = None):
        super().__init__(
            "",
            Entry(),
            name=name,
            style_focus="bold grey85",
            style_editing="bold cyan",
            style_unfocus="bold grey50",
        )
        self.focused = None

        from doit.utils.config import Config

        self.config = Config().load_config("todos")
        self.icons = self.config["icons"]

    async def _sort_by_arrangement(self, seq: list[int]) -> None:

        parent = self.highlighted_node.parent
        if not parent:
            return

        tree = parent.tree.children

        dup_tree = []
        node_tree = []
        for i in seq:
            dup_tree += (tree[i],)
            node_tree += (parent.children[i],)

        parent.tree.children = dup_tree.copy()
        parent.children = node_tree.copy()
        self.refresh()

    async def _sort(self, func: Callable, reverse: bool = False) -> None:

        parent = self.highlighted_node.parent
        if not parent:
            return

        dup = list(enumerate(parent.children))
        dup.sort(key=lambda x: func(x[1]), reverse=reverse)
        arrangemnt = [i for i, _ in dup]
        await self._sort_by_arrangement(arrangemnt)

    async def sort_by_urgency(self) -> None:
        await self._sort(
            func=lambda node: node.data.urgency,
            reverse=True,
        )

    async def sort_by_status(self) -> None:
        def f(status: str) -> int:
            match status:
                case "OVERDUE":
                    return 1
                case "PENDING":
                    return 2
                case "COMPLETED":
                    return 3
            return 0

        await self._sort(
            func=lambda node: f(node.data.status),
        )

    async def sort_by_name(self) -> None:
        await self._sort(
            func=lambda node: node.data.about.value,
        )

    # TODO
    async def sort_by_date(self) -> None:
        def f(date):
            if not date:
                return datetime.max
            else:
                return datetime(*self._parse_date(date))

        await self._sort(func=lambda node: f(node.data.due.value))

    async def sort_by(self, method: str) -> None:
        await eval(f"self.sort_by_{method}()")

    def _parse_date(self, date: str) -> tuple:
        day = int(date[:2])
        month = int(date[3:5])
        year = int(date[6:])

        return year, month, day

    def render(self) -> RenderableType:
        if self.root.tree.children:
            return self._tree
        else:
            return Align.center(
                EMPTY_TODO,
                vertical="middle",
                height=round(get_terminal_size()[1] * 0.8),
            )

    async def focus_node(self, part="about", status="INSERT") -> None:
        if self.highlighted == self.root.id:
            return

        self.focused = part
        self.prev_about = self.highlighted_node.data.about.value
        self.prev_date = self.highlighted_node.data.due.value

        await self.post_message(ChangeStatus(self, status))
        await super().focus_node(part)

        await self.post_message(
            events.Key(self, "right")
        )  # handle scrollview late update

    async def unfocus_node(self) -> None:
        await self.post_message(ChangeStatus(self, "NORMAL"))
        await self.check_node()
        await super().unfocus_node()

    async def modify_due_status(self, status: str) -> None:
        node = self.highlighted_node
        node.data.status = status

        parent = node.parent
        if parent and parent != self.root:
            if all(child.data.status == "COMPLETED" for child in parent.children):
                parent.data.status = "COMPLETED"
            else:
                parent.data.status = "PENDING"

        elif parent == self.root:
            if status == "COMPLETED":
                for i in node.children:
                    i.data.status = "COMPLETED"

        self.refresh()

    async def key_press(self, event: events.Key) -> None:
        if self.editing:
            match event.key:
                case "escape":
                    await self.unfocus_node()
                    await self.check_node()
                case _:
                    await self.send_key_to_selected(event)

        else:
            match event.key:
                case "j" | "down":
                    await self.cursor_down()
                case "J" | "shift+down":
                    await self.shift_down()
                case "k" | "up":
                    await self.cursor_up()
                case "K" | "shift+up":
                    await self.shift_up()
                case "g":
                    await self.move_to_top()
                case "G":
                    await self.move_to_bottom()
                case "z":
                    await self.toggle_expand()
                case "Z":
                    await self.toggle_expand_parent()
                case "A":
                    await self.add_child()
                case "a":
                    await self.add_sibling()
                case "i":
                    await self.focus_node("about", "INSERT")
                case "d":
                    await self.focus_node("due", "DATE")
                case "x":
                    await self.remove_node()
                case "c":
                    await self.mark_complete()
                case "+" | "=":
                    self.highlighted_node.data.increase_urgency()
                case "_" | "-":
                    self.highlighted_node.data.decrease_urgency()
                case "y":
                    try:
                        pyperclip.copy(self.highlighted_node.data.about.value)
                        await self.post_message(Notify(self, "Copied to Clipboard!"))
                    except:
                        await self.post_message(
                            Notify(self, "Cannot copy to Clipboard :(")
                        )

                case "ctrl+i":
                    if not self.editing:
                        await self.post_message(SwitchTab(self))

        self.refresh()

    async def mark_complete(self) -> None:
        await self.modify_due_status("COMPLETED")

    async def check_node(self) -> None:
        match self.focused:

            case "about":
                val = self.highlighted_node.data.about.value.strip()
                if not val:
                    if not self.prev_about:
                        await self.remove_node()
                    else:
                        self.highlighted_node.data.about.value = self.prev_about
                    await self.post_message(
                        Notify(self, "Can't leave todo's about empty :(")
                    )
                    return

                if (
                    sum(
                        i.data.about.value == val
                        for i in (self.highlighted_node.parent or self.root).children
                    )
                    > 1
                ):
                    await self.remove_node()
                    await self.post_message(Notify(self, "Duplicate todo sibling !"))
                    return

            case "due":
                date = self.highlighted_node.data.due.value

                if len(date) == 10 and re.findall(r"^\d\d-\d\d-\d\d\d\d$", date):
                    if not self._is_valid_date(date):
                        await self.post_message(
                            Notify(self, message="Please enter a valid date")
                        )
                        self.highlighted_node.data.due.value = self.prev_date
                    else:
                        await self.post_message(
                            Notify(self, message="You due date was updated")
                        )
                        await self.update_due_status()

                else:
                    await self.post_message(
                        Notify(
                            self,
                            message="Invalid date format! Enter in format: dd-mm-yyyy",
                        )
                    )

                    self.highlighted_node.data.due.value = self.prev_date

        self.focused = None
        self.refresh()

    def _is_valid_date(self, date: str) -> bool:
        try:
            datetime(*self._parse_date(date))
            return True
        except ValueError:
            return False

    def _is_expired(self, date) -> bool:
        present = datetime.now()
        due = datetime(*self._parse_date(date))

        return due < present

    async def update_due_status(self) -> None:
        date = self.highlighted_node.data.due.value
        status = self.highlighted_node.data.status

        if status == "COMPLETED":
            return

        if date and self._is_expired(date):
            await self.modify_due_status("OVERDUE")
        else:
            await self.modify_due_status("PENDING")

    def _about_width(self, child: bool):
        return percentage(60, self.size.width) - 6 - (child * 3)

    def _due_width(self, child: bool):
        return percentage(30, self.size.width) - 6 - (child * 3)

    def _get_entry(self, child: bool) -> Entry:
        entry = NodeDataTye()
        entry.about.view = View(0, percentage(60, self.size.width) - 6 - (child * 3))
        entry.due.view = View(0, percentage(30, self.size.width) - 6 - (child * 3))
        return entry

    async def reach_to_node(self, id: TreeNode | NodeID) -> None:

        if isinstance(id, TreeNode):
            id = id.id

        if self.nodes[id] in self.root.children:
            await self.move_to_top()
            while self.highlighted != id:
                await self.cursor_down()
        else:
            await self.reach_to_node(self.nodes[id].parent)
            await self.highlighted_node.expand()
            while self.highlighted != id:
                await self.cursor_down()

    async def add_child(self) -> None:
        node = self.highlighted_node
        if node == self.root or node.parent == self.root:
            await node.add("child", self._get_entry(node != self.root))
            await node.expand()
            await self.reach_to_last_child()
            await self.focus_node()
            self.refresh(layout=True)

    async def add_sibling(self) -> None:
        parent = self.highlighted_node.parent

        if not parent:
            await self.add_child()
            return
        else:
            children = parent.children
            tree = parent.tree.children

            await parent.add("", self._get_entry(child=parent != self.root))
            i = children.index(self.highlighted_node)
            children.insert(i + 1, children.pop())
            tree.insert(i + 1, tree.pop())
            await self.cursor_down()

        await self.focus_node()
        self.refresh()

    def render_node(self, node: TreeNode) -> RenderableType:
        """
        Renders styled node
        """

        from rich.table import Table

        table = Table.grid(padding=(0, 1), expand=True)
        table.add_column("about", justify="left", ratio=60)
        table.add_column("due", justify="left", ratio=30)
        table.add_column("urgency", justify="left", ratio=10)

        color = "yellow"
        match node.data.status:
            case "COMPLETED":
                color = "green"
            case "OVERDUE":
                color = "red"

        table.add_row(
            self.render_about(node, color),
            self.render_date(node, color),
            self.render_priority(node, color),
        )

        return table

    def _highlight_node(self, node: TreeNode, label: Text) -> Text:
        # setup highlight
        style_editing = self.config["theme"]["style_editing"]
        style_focused = self.config["theme"]["style_focused"]
        style_unfocused = self.config["theme"]["style_unfocused"]

        if node.id == self.highlighted:
            if self.editing:
                label.stylize(style_editing)
            else:
                label.stylize(style_focused)
        else:
            label.stylize(style_unfocused)

        if node.data.status == "COMPLETED":
            label.stylize("strike")

        return label

    def render_about(self, node, _) -> Text:
        # Setting up text

        width = self._about_width(node.parent != self.root)
        if (
            not hasattr(node.data.about, "view")
        ) or node.data.about.view.end - node.data.about.view.start != width:
            node.data.about.view = View(0, width)

        label = Text.from_markup(str(node.data.about.render())) or Text()
        label = self._highlight_node(node, label)

        # setup milestone
        if children := node.children:
            total = len(children)
            done = sum(child.data.status == "COMPLETED" for child in children)

            if not (self.highlighted_node == node and self.editing):
                label += Text.from_markup(f" ( [green][/green] {done}/{total} )")

        # setup pre-icons
        if node != self.root:
            match node.data.status:
                case "COMPLETED":
                    label = (
                        Text.from_markup(
                            f"[b green]{self.icons['todo_completed']}  [/b green]"
                        )
                        + label
                    )
                case "PENDING":
                    label = (
                        Text.from_markup(
                            f"[b yellow]{self.icons['todo_pending']}  [/b yellow]"
                        )
                        + label
                    )
                case "OVERDUE":
                    label = (
                        Text.from_markup(
                            f"[b red]{self.icons['todo_overdue']}  [/b red]"
                        )
                        + label
                    )

        meta = {
            "@click": "click_about()",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)
        return label

    def render_date(self, node: TreeNode, color) -> Text:

        icon = self.icons["due_date"]

        width = self._due_width(node.parent != self.root)
        if (
            not hasattr(node.data.due, "view")
        ) or node.data.due.view.end - node.data.due.view.start != width:
            node.data.due.view = View(0, width)

        label = Text.from_markup(str(node.data.due.render())) or Text("No Due Date")
        label = self._highlight_node(node, label)
        label = Text.from_markup(f"[{color}]  {icon}  [/{color}]") + label

        meta = {
            "@click": "click_date()",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)
        return label

    def render_priority(self, node: TreeNode, color) -> Text:

        icon = self.icons["urgency"]

        label = Text(str(node.data.urgency))
        label.plain = label.plain.rjust(3, "0")
        label = self._highlight_node(node, label)
        label = Text.from_markup(f"[{color}]{icon} [/{color}]") + label
        return label

    async def action_click_date(self) -> None:
        await self.focus_node("due", "DATE")

    async def action_click_about(self) -> None:
        await self.focus_node("about", "INSERT")
