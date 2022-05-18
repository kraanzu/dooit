from rich.console import RenderableType
from rich.text import Text
from textual import events
from doit.ui.widgets.tree_edit import TreeEdit
from textual.widgets import TreeNode


class UrgencyTree(TreeEdit):
    async def handle_keypress(self, event: events.Key) -> None:
        if event.key != "i":
            return await super().handle_keypress(event)

    def render_node(self, node: TreeNode) -> RenderableType:

        color = "yellow"
        if data := node.data:
            label = Text(f"{data.todo.urgency} ")
            match node.data.todo.due:
                case "COMPLETE":
                    color = "green"

                case "OVERDUE":
                    color = "red"
        else:
            label = Text()

        label = Text.from_markup(f"[{color}]   [/{color}]") + label

        if node.id == self.highlighted:
            label.stylize("bold reverse red")

        # label.justify = "center"
        label.append("   ")

        return label
