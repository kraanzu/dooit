from rich.console import RenderableType
from rich.text import Text
from textual.widgets import TreeNode

from . import DateTree


class UrgencyTree(DateTree):
    """
    A class to show a tree with current set urgency
    """

    async def handle_key(self, key: str) -> None:

        match key:
            case "+" | "=":
                self.nodes[self.highlighted].data.increase_urgency()
            case "-" | "_":
                self.nodes[self.highlighted].data.increase_urgency()

        return await super().handle_key(key)

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
