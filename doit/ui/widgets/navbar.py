from rich.console import Console, RenderableType
from rich.text import Text
from doit.ui.widgets.todo_list import TreeEdit
from textual.widgets import TreeNode


class Navbar(TreeEdit):
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
