from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode
from textual_extras.events import ListItemSelected
from textual_extras.widgets.single_level_tree_edit import SimpleInput
from textual_extras.widgets.text_input import View
from doit.ui.events.events import ModifyTopic

from doit.ui.widgets import Entry, NestedListEdit


class Navbar(NestedListEdit):
    """
    A widget to show the todo menu
    """

    def __init__(self):
        super().__init__("", Entry())
        self.lineno = 0

    def render(self):
        return self._tree

    def _get_node_path(self):

        path = ""
        node = self.nodes[self.highlighted]
        while node.parent:
            path = f"{node.data.value}/{path}"
            node = node.parent

        return path

    def render_node(self, node: TreeNode) -> RenderableType:

        if not hasattr(node.data, "view"):
            node.data.view = View(0, self.size.width - 6)

        return self.render_custom_node(node)

    async def focus_node(self) -> None:
        self._last_path = self._get_node_path()
        self.nodes[self.highlighted].data.on_focus()
        self.editing = True

    async def unfocus_node(self) -> None:
        await self.post_message(
            ModifyTopic(self, self._last_path, self._get_node_path())
        )
        self.nodes[self.highlighted].data.on_blur()
        self.editing = False

    async def send_key_to_selected(self, event: events.Key) -> None:
        await self.nodes[self.highlighted].data.on_key(event)

    async def key_press(self, event: events.Key):
        if not self.editing and event.key == "enter":
            await self.emit(ListItemSelected(self, self._get_node_path()))
        await super().key_press(event)

    def get_box(self):
        a = SimpleInput()
        a.view = View(0, self.size.width - 6)
        return a

    async def add_child(self):
        node = self.nodes[self.highlighted]
        if node == self.root or node.parent == self.root:
            node = self.nodes[self.highlighted]
            await node.add("child", self.get_box())
            await node.expand()
            await self.reach_to_last_child()
            await self.focus_node()

        self.refresh()

    async def add_sibling(self) -> None:
        if self.nodes[self.highlighted].parent == self.root:
            await self.root.add("child", self.get_box())
            await self.move_to_bottom()
        else:
            await self.reach_to_parent()
            await self.add_child()
        await self.focus_node()
        self.refresh()

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
