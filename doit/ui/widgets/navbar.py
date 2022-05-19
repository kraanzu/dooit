from rich.console import RenderableType
from rich.text import Text
from textual.widgets import TreeNode
from . import TreeEdit


class Navbar(TreeEdit):
    """
    A widget to show the todo menu
    """

    def render_node(self, node: TreeNode) -> RenderableType:

        if data := node.data:
            try:
                label = Text.from_markup(str(data.render()))
            except:
                label = Text(str(data.render()))
        else:
            label = Text()

        if node.id == self.highlighted:
            label.stylize("bold red")

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)
        return label
