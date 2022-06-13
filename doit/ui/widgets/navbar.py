from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode
from doit.ui.events.events import ChangeStatus

from doit.ui.widgets.simple_input import SimpleInput, View

from ...ui.events import ModifyTopic, ListItemSelected
from ...ui.widgets import NestedListEdit


class Navbar(NestedListEdit):
    """
    A widget to show the todo menu
    """

    def __init__(self):
        super().__init__("", SimpleInput())

    def render(self) -> RenderableType:
        return self._tree

    def _get_node_path(self):

        path = ""
        node = self.highlighted_node
        while node.parent:
            path = f"{node.data.value}/{path}"
            node = node.parent

        return path

    def render_node(self, node: TreeNode) -> RenderableType:

        width = self._get_width(node.parent != self.root)
        if (
            not hasattr(node.data, "view")
            or node.data.view.end - node.data.view.start != width
        ):
            node.data.view = View(0, width)

        return self.render_custom_node(node)

    async def focus_node(self) -> None:
        self._last_path = self._get_node_path()
        self.highlighted_node.data.on_focus()
        await self.post_message(ChangeStatus(self, "INSERT"))
        self.editing = True

    async def unfocus_node(self) -> None:
        await self.post_message(
            ModifyTopic(self, self._last_path, self._get_node_path()),
        )
        await self.post_message(ChangeStatus(self, "NORMAL"))
        self.highlighted_node.data.on_blur()
        self.editing = False

    async def send_key_to_selected(self, event: events.Key) -> None:
        await self.highlighted_node.data.on_key(event)

    async def key_press(self, event: events.Key):
        if not self.editing and event.key == "enter":
            await self.post_message(
                ListItemSelected(
                    self,
                    self._get_node_path(),
                    focus=True,
                )
            )
            self.refresh()
            return

        await super().key_press(event)

        # REASON: RENDERING ISSUES
        if self.highlighted != self.root.id and not self.editing:
            await self.emit(
                ListItemSelected(
                    self,
                    self._get_node_path(),
                    focus=False,
                )
            )
        self.refresh()

    def _get_width(self, child: bool):
        width = self.size.width - 6
        if child:
            width -= 3
        return width

    def get_ibox(self, child: bool = False):
        ibox = SimpleInput()
        width = self._get_width(child)
        ibox.view = View(0, width)
        return ibox

    async def add_child(self) -> None:
        """
        Adds child to current selected node
        """

        node = self.highlighted_node
        if node == self.root or node.parent == self.root:
            node = self.highlighted_node
            await node.add(
                "child",
                self.get_ibox(child=node != self.root),
            )
            await node.expand()
            await self.reach_to_last_child()
            await self.focus_node()

        self.refresh()

    async def add_sibling(self) -> None:
        """
        Adds sibling for the currently selected node
        """

        if self.highlighted_node.parent == self.root:
            await self.root.add("child", self.get_ibox(child=False))
            await self.move_to_bottom()
        else:
            await self.reach_to_parent()
            await self.add_child()
        await self.focus_node()
        self.refresh()

    def render_custom_node(self, node: TreeNode) -> RenderableType:
        # return str(node.data.view)

        label = Text.from_markup(str(node.data.render()) or "")
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
        label.pad_right(self.size.width)
        if node.id == self.highlighted:
            label.stylize("bold reverse red")

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)
        return label
