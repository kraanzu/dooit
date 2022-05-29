from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode
from textual_extras.widgets.nested_list_edit import NestedListEdit
from textual_extras.widgets.text_input import View

from ...ui.widgets.entry import Entry
from ...ui.events import *

NodeDataTye = Entry


class TodoList(NestedListEdit):
    """
    A Class that allows editing while displaying trees
    """

    def __init__(self):
        super().__init__("", Entry())

    def render(self):
        return self._tree

    async def focus_node(self) -> None:
        await self.post_message(ChangeStatus(self, "INSERT"))
        return super().focus_node()

    async def unfocus_node(self):
        await self.post_message(ChangeStatus(self, "NORMAL"))
        return super().unfocus_node()

    async def on_key(self, event: events.Key):
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
                case 'x':
                    await self.remove_node()


        self.refresh()

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

        # fix padding
        label.plain = " " + label.plain
        label.pad_right(self.size.width, " ")

        # setup highlight
        if node.id == self.highlighted:
            if self.editing:
                label.stylize(self.style_editing)
            else:
                label.stylize(self.style_focus)
        else:
            label.stylize(self.style_unfocus)

        # setup pre-icons
        if node != self.root:
            match node.data.todo.status:
                case "COMPLETE":
                    label = Text.from_markup(" [b green] [/b green]") + label
                case "PENDING":
                    label = Text.from_markup(" [b yellow] [/b yellow]") + label
                case "OVERDUE":
                    label = Text.from_markup(" [b yellow] [/b yellow]") + label

        # setup milestone
        if children := node.children:
            total = len(children)
            done = sum(child.data.todo.status == "COMPLETE" for child in children)
            label.append(Text.from_markup(f" ( [green][/green] {done}/{total} )"))
        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)

        return label
