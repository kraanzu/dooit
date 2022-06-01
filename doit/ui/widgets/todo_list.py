from datetime import datetime
from typing import Callable
from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode
from textual_extras.widgets.text_input import View

from doit.ui.widgets.nested_list_edit import NestedListEdit

from ...ui.widgets.entry import Entry
from ...ui.events import *

NodeDataTye = Entry


def percentage(percent, total):
    return round(percent * total / 100)


class TodoList(NestedListEdit):
    """
    A Class that allows editing while displaying trees
    """

    def __init__(self):
        super().__init__(
            "",
            Entry(),
            style_focus="bold grey85",
            style_editing="bold cyan",
            style_unfocus="bold grey50",
        )

    async def on_click(self, event: events.Click) -> None:
        await self.post_message(FocusTodo(self))
        return await super().on_click(event)

    async def _sort_by_arrangement(self, seq: list[int]):

        parent = self.nodes[self.highlighted].parent
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

    async def _sort(self, func: Callable):

        parent = self.nodes[self.highlighted].parent
        if not parent:
            return

        dup = list(enumerate(parent.children))
        dup.sort(key=lambda x: func(x[1]))
        arrangemnt = [i for i, _ in dup]

        await self.post_message(SortNodes(self, arrangemnt))
        # await self._sort_by_arrangement([i for i, _ in dup])

    async def sort_by_urgency(self):
        await self._sort(
            func=lambda node: node.data.urgency,
        )

    async def sort_by_status(self):
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

    async def sort_by_name(self):
        await self._sort(
            func=lambda node: node.data.value,
        )

    # TODO
    async def sort_by_date(self):
        def f(date):
            if not date:
                return datetime(1, 1, 1)
            else:
                return datetime(*self._parse_date(date))

        await self._sort(func=lambda node: f(node.data.due))

    async def sort_by(self, method: str):
        await eval(f"self.sort_by_{method}()")

    def _parse_date(self, date: str) -> tuple:
        day = int(date[:2])
        month = int(date[3:5])
        year = int(date[6:])

        return year, month, day

    def update_date(self, date):
        self.nodes[self.highlighted].data.due = date

    def render(self):
        return self._tree

    async def focus_node(self, part="about", status="INSERT") -> None:
        await self.post_message(ChangeStatus(self, status))
        await super().focus_node(part)

    async def unfocus_node(self):
        await self.post_message(ChangeStatus(self, "NORMAL"))
        await super().unfocus_node()

    async def modify_due_status(self, event: ModifyDue):
        node = self.nodes[self.highlighted]
        node.data.status = event.status

        parent = node.parent
        if parent and parent != self.root:
            if all(child.data.status == "COMPLETED" for child in parent.children):
                parent.data.status = "COMPLETED"

        elif parent == self.root:
            if event.status == "COMPLETED":
                for i in node.children:
                    i.data.status = "COMPLETED"

        self.refresh()

    async def key_press(self, event: events.Key):
        if self.editing:
            match event.key:
                case "escape":
                    await self.unfocus_node()
                    await self.check_node_about()
                case _:
                    await self.send_key_to_selected(event)

        else:
            match event.key:
                case "p":
                    await self.sort_by_name()
                case "j" | "down":
                    await self.cursor_down()
                case "k" | "up":
                    await self.cursor_up()
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
                    self.nodes[self.highlighted].data.increase_urgency()
                case "_" | "-":
                    self.nodes[self.highlighted].data.decrease_urgency()

        self.refresh()

    async def mark_complete(self):
        await self.post_message(ModifyDue(self, "COMPLETED"))

    async def check_node_about(self):
        node = self.nodes[self.highlighted]
        if not str(node.data.about.render()).strip():
            await self.emit(events.Key(self, "x"))

    def get_box(self):
        a = NodeDataTye()
        a.about.view = View(0, percentage(60, self.size.width) - 6)
        a.due.view = View(0, percentage(30, self.size.width) - 6)
        return a

    async def add_child(self):
        node = self.nodes[self.highlighted]
        if node == self.root or node.parent == self.root:
            await node.add("child", self.get_box())
            await node.expand()
            await self.reach_to_last_child()
            await self.focus_node()

    async def add_sibling(self):
        if self.nodes[self.highlighted].parent == self.root:
            await self.root.add("child", self.get_box())
            await self.move_to_bottom()
        else:
            await self.reach_to_parent()
            await self.add_child()
        await self.focus_node()

    def render_node(self, node: TreeNode) -> RenderableType:
        """
        Renders styled node
        """

        from rich.table import Table

        table = Table.grid(padding=(0, 1), expand=True)
        table.add_column("about", justify="left", ratio=60)
        table.add_column("due", justify="left", ratio=30)
        table.add_column("urgency", justify="left", ratio=10)

        table.add_row(
            self.render_about(node),
            self.render_date(node),
            self.render_urgency(node),
        )

        return table

    def render_about(self, node) -> RenderableType:
        # Setting up text
        if data := node.data:
            try:
                label = Text.from_markup(
                    str(data.about.render()),
                )
            except:
                label = Text(str(data.about.render()))
        else:
            label = Text()

        # setup highlight
        if node.id == self.highlighted:
            if self.editing:
                label.stylize(self.style_editing)
            else:
                label.stylize(self.style_focus)
        else:
            label.stylize(self.style_unfocus)

        # setup milestone
        if children := node.children:
            total = len(children)
            done = sum(child.data.status == "COMPLETED" for child in children)
            label += Text.from_markup(f" ( [green][/green] {done}/{total} )")

        # setup pre-icons
        if node != self.root:
            match node.data.status:
                case "COMPLETED":
                    label.stylize("strike")
                    label = Text.from_markup("[b green]  [/b green]") + label
                case "PENDING":
                    label = Text.from_markup("[b yellow]  [/b yellow]") + label
                case "OVERDUE":
                    label = Text.from_markup("[b red]  [/b red]") + label

        # fix padding
        # label.pad_right(self.size.width)

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)

        return label

    def render_date(self, node: TreeNode) -> RenderableType:
        color = "yellow"
        match node.data.status:
            case "COMPLETED":
                color = "green"
            case "OVERDUE":
                color = "red"

        # Setting up text
        label = Text.from_markup(
            str(node.data.due.render()),
        )

        if not label.plain:
            label = Text("Until You Die")

        if node.id == self.highlighted:
            if self.editing:
                label.stylize(self.style_editing)
            else:
                label.stylize(self.style_focus)
        else:
            label.stylize(self.style_unfocus)

        # label = label[:13]

        # SAFETY: color will never be unbound
        # because the match statement in exhaustive
        if color == "green":
            label.stylize("strike")

        label = Text.from_markup(f"[{color}]  [/{color}]") + label

        return label

    def render_urgency(self, node: TreeNode) -> RenderableType:

        color = "yellow"
        match node.data.status:
            case "COMPLETED":
                color = "green"
            case "OVERDUE":
                color = "red"

        # Setting up text
        label = Text.from_markup(
            str(node.data.urgency),
        )

        label.plain = label.plain.rjust(3, "0")
        label = Text(" ") + label + " "

        if node.id == self.highlighted:
            if self.editing:
                label.stylize(self.style_editing)
            else:
                label.stylize(self.style_focus)
        else:
            label.stylize(self.style_unfocus)

        # SAFETY: color will never be unbound
        # because the match statement in exhaustive

        if color == "green":
            label.stylize("strike")

        label = Text.from_markup(f"[{color}] [/{color}]") + label

        return label
