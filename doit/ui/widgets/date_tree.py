from typing import Literal
from rich.console import RenderableType
from rich.text import Text
from textual import events
from doit.ui.widgets.entry import Entry
from doit.ui.widgets.tree_edit import TreeEdit
from textual.widgets import TreeNode


class DateTree(TreeEdit):
    async def handle_shortcut(self, key: str):
        async def reach_to_node(node: TreeNode, direction: Literal["up", "down"]):
            while self.highlighted != node.id:
                await self.handle_shortcut(direction)

        match key:
            case "g":
                while self.highlighted != self.root.children[0].id:
                    await self.handle_shortcut("k")

            case "G":
                while self.highlighted != self.root.children[-1].id:
                    await self.handle_shortcut("j")

            case "a":
                node = self.nodes[self.highlighted]
                await node.add("", Entry())
                await node.expand()
                await reach_to_node(node.children[-1], "down")

            case "A":
                node = self.nodes[self.highlighted]
                if node.parent == self.root:
                    await self.root.add("", Entry())
                    await self.handle_shortcut("G")
                else:
                    # SAFETY: root parent case has already been handled above
                    await reach_to_node(node.parent, "up")
                    await self.handle_shortcut("a")

            case "c":
                self.nodes[self.highlighted].data.mark_complete()

            case "x":
                await self.remove(self.highlighted)

            case "z":
                if self.highlighted:
                    node = self.nodes[self.highlighted]
                    await node.toggle()

            case "Z":
                if parent := self.nodes[self.highlighted].parent:
                    if parent != self.root:
                        while self.nodes[self.highlighted].previous_node != parent:
                            await self.handle_shortcut("k")

                        await self.handle_shortcut("k")
                        await self.handle_shortcut("z")

            case "j" | "down":
                await self.move_highlight_down()

            case "k" | "up":
                await self.move_highlight_up()

    def render_node(self, node: TreeNode) -> RenderableType:

        color = "yellow"

        if data := node.data:
            label = Text(str(data.todo.due))
            match node.data.todo.due:
                case "COMPLETE":
                    color = "green"

                case "OVERDUE":
                    color = "red"
        else:
            label = Text()

        if not label.plain:
            label = Text("No due date")

        label = Text.from_markup(f"[{color}]   [/{color}]") + label
        label.append(" ")

        if node.id == self.highlighted:
            label.stylize("bold reverse red")

        return label
