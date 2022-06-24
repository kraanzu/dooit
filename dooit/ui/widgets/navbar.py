from os import get_terminal_size
from rich.align import Align
from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode, NodeID

from ...ui.widgets.simple_input import SimpleInput, View
from ...ui.events import (
    ModifyTopic,
    ListItemSelected,
    ChangeStatus,
    Notify,
    RemoveTopic,
)
from ...ui.widgets import NestedListEdit

EMPTY_TOPIC = Text.from_markup(
    """
Nothing yet?
Press [b yellow]'a'[/b yellow] to add a topic
""",
    style="dim white",
)
WARNING = "[b yellow]WARNING[/b yellow]"


class Navbar(NestedListEdit):
    """
    A widget to show the todo menu
    """

    def __init__(self):
        super().__init__("", SimpleInput())
        from dooit.utils.config import conf

        self.config = conf.load_config("menu")
        self.select_key = conf.keys.select_node

    def render(self) -> RenderableType:
        if self.root.tree.children:
            return self._tree
        else:
            return Align.center(
                EMPTY_TOPIC,
                vertical="middle",
                height=round(0.8 * get_terminal_size()[1]),
            )

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
        self.prev_value = self.highlighted_node.data.value
        self._last_path = self._get_node_path()
        self.highlighted_node.data.on_focus()
        self.warn = False
        await self.highlighted_node.data.handle_keypress("end")
        await self.post_message(ChangeStatus(self, "INSERT"))
        self.editing = True

    async def remove_node(self, id: NodeID | None = None) -> None:
        await self.post_message(RemoveTopic(self, self._get_node_path()))
        await super().remove_node(id)

    async def check_node(self) -> bool:
        val = self.highlighted_node.data.value.strip()
        if not val:
            if not self.prev_value:
                await self.remove_node()
                await self.post_message(
                    Notify(self, f"{WARNING}: Empty topic! Deleted")
                )
                return True
            else:
                self.highlighted_node.data.value = self.prev_value
                await self.post_message(
                    Notify(self, f"{WARNING}: Can't leave topic name empty")
                )
                return True

        if (
            sum(
                i.data.value == val
                for i in (self.highlighted_node.parent or self.root).children
            )
            > 1
        ):

            await self.post_message(
                Notify(
                    self,
                    f"{WARNING}: Duplicate sibling topic!"
                    if not self.warn
                    else "Topic Deleted!",
                )
            )
            return False

        return True

    async def unfocus_node(self) -> None:
        await self.post_message(
            ModifyTopic(self, self._last_path, self._get_node_path()),
        )

        ok = await self.check_node()
        if not ok:
            if self.warn:
                await self.remove_node()
            else:
                self.warn = True
                return

        await self.post_message(ChangeStatus(self, "NORMAL"))
        await self.highlighted_node.data.handle_keypress("home")
        self.highlighted_node.data.on_blur()
        self.editing = False

    async def send_key_to_selected(self, event: events.Key) -> None:
        await self.highlighted_node.data.on_key(event)

    async def key_press(self, event: events.Key):
        if (
            not self.editing
            and self.highlighted_node != self.root
            and event.key in self.select_key
        ):
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

        parent = self.highlighted_node.parent

        if not parent:
            await self.add_child()
            return
        else:
            children = parent.children
            tree = parent.tree.children

            await parent.add("", self.get_ibox(child=parent != self.root))
            i = children.index(self.highlighted_node)
            id = children[-1].id
            children.insert(i + 1, children.pop())
            tree.insert(i + 1, tree.pop())

            while self.highlighted != id:
                await self.cursor_down()

        await self.focus_node()
        self.refresh()

    def render_custom_node(self, node: TreeNode) -> RenderableType:
        icons = self.config["icons"]
        colors = self.config["theme"]

        label = Text.from_markup(str(node.data.render()) or "")
        label.plain = label.plain[: self.size.width - 2]

        # Setup pre-icons
        if node.children:
            if not node.expanded:
                icon = icons["nested_close"]
            else:
                icon = icons["nested_open"]
        else:
            icon = icons["single_topic"]

        # Padding adjustment
        label.plain = f" {icon} " + label.plain + " "
        label.pad_right(self.size.width)

        if node.id == self.highlighted:
            if self.editing:
                label.stylize(colors["style_editing"])
            else:
                label.stylize(colors["style_focused"])
        else:
            label.stylize(colors["style_unfocused"])

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)
        return label

    async def handle_tree_click(self, *_) -> None:
        await self.post_message(
            ListItemSelected(
                self,
                self._get_node_path(),
                focus=True,
            )
        )
