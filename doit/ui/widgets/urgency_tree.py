from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode

from . import TodoList


class UrgencyTree(TodoList):
    """
    A class to show a tree with current set urgency
    """

    async def add_child(self):
        node = self.nodes[self.highlighted]
        if node == self.root or node.parent == self.root:
            await node.add("child", self.get_box())
            await node.expand()
            await self.reach_to_last_child()

    async def add_sibling(self):
        if self.nodes[self.highlighted].parent == self.root:
            await self.root.add("child", self.get_box())
            await self.move_to_bottom()
        else:
            await self.reach_to_parent()
            await self.add_child()

    async def on_key(self, event: events.Key) -> None:
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
            # case "i":
            #     await self.focus_node()
            case "x":
                await self.remove_node()
            case "+" | "=":
                self.nodes[self.highlighted].data.increase_urgency()
            case "-" | "_":
                self.nodes[self.highlighted].data.decrease_urgency()

        self.refresh()

    #
    def render_node(self, node: TreeNode) -> RenderableType:
        color = "yellow"

        # setup text
        label = Text()
        if data := node.data:
            label = Text(f"{data.todo.urgency}")
            match node.data.todo.due:
                case "COMPLETE":
                    color = "green"

                case "OVERDUE":
                    color = "red"

        label.plain = label.plain.rjust(3, "0")
        label = Text(" ") + label + " "

        if node.id == self.highlighted:
            label.stylize("bold reverse blue")

        label = Text.from_markup(f"[{color}]   [/{color}]") + label
        return label
