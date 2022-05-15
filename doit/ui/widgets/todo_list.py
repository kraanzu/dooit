from rich.console import RenderableType
from rich.text import Text
from textual.widgets import TreeNode
from ...ui.widgets.tree_edit import TreeEdit


class TodoList(TreeEdit):
    """
    A Class that allows editing while displaying trees
    """

    def render_node(self, node: TreeNode) -> RenderableType:
        """
        Renders styled node
        """

        if data := node.data:
            try:
                label = Text.from_markup(
                    str(data.render()),
                )
            except:
                label = Text(str(data.render()))
        else:
            label = Text()

        if node.id == self.selected:
            label.stylize("bold cyan")
        elif node.id == self.highlighted:
            label.stylize("bold magenta")

        if node != self.root:
            match node.data.todo.status:
                case "COMPLETE":
                    label = Text.from_markup("[b green] [/b green]") + label
                case "PENDING":
                    label = Text.from_markup("[b yellow] [/b yellow]") + label
                case "OVERDUE":
                    label = Text.from_markup("[b yellow] [/b yellow]") + label

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
