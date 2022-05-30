from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode
from textual_extras.events import ListItemSelected

from doit.ui.widgets import Entry, NestedListEdit


class Navbar(NestedListEdit):
    """
    A widget to show the todo menu
    """

    def __init__(self):
        super().__init__("", Entry())

    def render(self):
        return self._tree

    async def key_press(self, event: events.Key):
        if not self.editing and event.key == "enter":
            await self.emit(
                ListItemSelected(self, self.nodes[self.highlighted].data.value)
            )
        await super().key_press(event)

    async def add_child(self):
        node = self.nodes[self.highlighted]
        if node == self.root or node.parent == self.root:
            return await super().add_child()

    def render_custom_node(self, node: TreeNode) -> RenderableType:

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
