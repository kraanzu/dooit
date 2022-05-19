from rich.console import RenderableType
from rich.text import Text
from textual.widgets import TreeNode

from . import DateTree


class UrgencyTree(DateTree):
    """
    A class to show a tree with current set urgency
    """

    def render_node(self, node: TreeNode) -> RenderableType:
        color = "yellow"
        label = Text()
        if data := node.data:
            label = Text(f"{data.todo.urgency}")
            match node.data.todo.due:
                case "COMPLETE":
                    color = "green"

                case "OVERDUE":
                    color = "red"

        label = Text(" ") + label + " "
        if node.id == self.highlighted:
            label.stylize("bold reverse blue")

        label = Text.from_markup(f"[{color}]   [/{color}]") + label
        return label
