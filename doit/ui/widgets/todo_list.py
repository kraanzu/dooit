from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode
from textual_extras.widgets.text_input import View

from doit.ui.widgets.nested_list_edit import NestedListEdit

from ...ui.widgets.entry import Entry
from ...ui.events import *

NodeDataTye = Entry


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

    def render(self):
        return self._tree

    async def focus_node(self) -> None:
        await self.post_message(ChangeStatus(self, "INSERT"))
        await super().focus_node()

    async def unfocus_node(self):
        await self.post_message(ChangeStatus(self, "NORMAL"))
        await super().unfocus_node()

    async def modify_due_status(self, event: ModifyDue):
        node = self.nodes[self.highlighted]
        node.data.todo.status = event.status

        parent = node.parent
        if parent and parent != self.root:
            if all(child.data.todo.status == "COMPLETED" for child in parent.children):
                parent.data.todo.status = "COMPLETED"

        elif parent == self.root:
            if event.status == "COMPLETED":
                for i in node.children:
                    i.data.todo.status = "COMPLETED"

        self.refresh()

    async def key_press(self, event: events.Key):
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
                    await self.focus_node()
                case "x":
                    await self.remove_node()
                case "c":
                    await self.mark_complete()

        self.refresh()

    async def mark_complete(self):
        await self.post_message(ModifyDue(self, "COMPLETED"))

    async def check_node(self):
        node = self.nodes[self.highlighted]
        if not str(node.data.render()).strip():
            await self.emit(events.Key(self, "x"))

    def get_box(self):
        a = NodeDataTye()
        a.view = View(0, self.size.width - 6)
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

    def render_custom_node(self, node: TreeNode) -> RenderableType:
        """
        Renders styled node
        """

        # Setting up text
        if data := node.data:
            try:
                label = Text.from_markup(
                    str(data.render()),
                )
            except:
                label = Text(str(data.render()))
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
            done = sum(child.data.todo.status == "COMPLETED" for child in children)
            label += Text.from_markup(f" ( [green][/green] {done}/{total} )")

        # setup pre-icons
        if node != self.root:
            match node.data.todo.status:
                case "COMPLETED":
                    label.stylize("strike")
                    label = Text.from_markup("[b green]  [/b green]") + label
                case "PENDING":
                    label = Text.from_markup("[b yellow]  [/b yellow]") + label
                case "OVERDUE":
                    label = Text.from_markup("[b red]  [/b red]") + label

        # fix padding
        label.pad_right(self.size.width)

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)

        return label
