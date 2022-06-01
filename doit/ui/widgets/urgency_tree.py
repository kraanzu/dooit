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
            await node.add("child", self._get_entry())
            await node.expand()
            await self.reach_to_last_child()

    async def add_sibling(self):
        if self.nodes[self.highlighted].parent == self.root:
            await self.root.add("child", self._get_entry())
            await self.move_to_bottom()
        else:
            await self.reach_to_parent()
            await self.add_child()

    async def key_press(self, event: events.Key) -> None:

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
            case "x":
                await self.remove_node()
            case "+" | "=":
                self.nodes[self.highlighted].data.increase_urgency()
            case "-" | "_":
                self.nodes[self.highlighted].data.decrease_urgency()

        self.refresh()

    #
    def render_node(self, node: TreeNode) -> RenderableType:

        match node.data.status:
            case "PENDING":
                color = "yellow"
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
