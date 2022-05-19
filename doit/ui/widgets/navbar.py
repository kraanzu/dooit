from rich.console import RenderableType
from rich.text import Text
from textual.widgets import TreeNode
from . import TreeEdit


class Navbar(TreeEdit):
    """
    A widget to show the todo menu
    """

    def render_node(self, node: TreeNode) -> RenderableType:

        # Gather text
        if data := node.data:
            try:
                label = Text.from_markup(str(data.render()))
            except:
                label = Text(str(data.render()))
        else:
            label = Text()

        # Trim to fit the size
        label.plain = label.plain[: self.size.width - 2]

        # Setup pre-icons
        if node.children:
            if node.expanded:
                icon = "ﱮ"
            else:
                icon = ""
        else:
            icon = ""

        # Padding adjustment
        label.plain = f" {icon} " + label.plain + " "
        label.pad_right(self.size.width, " ")

        # Highlights
        if node.id == self.highlighted:
            label.stylize("bold reverse red")

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)
        return label
