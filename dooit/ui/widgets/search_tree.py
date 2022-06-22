from os import get_terminal_size
from rich.align import Align
from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import NodeID, TreeNode

from ...ui.events.events import ChangeStatus, HighlightNode
from ...ui.widgets.simple_input import SimpleInput, View
from ...ui.widgets.todo_list import TodoList

NO_MATCH = """
                    [blue][/blue]
                [d white]0 matches
Nothing showed up?! Maybe try somthing different?[/d white]
"""


class SearchTree(TodoList):
    """
    A tree with built in searching
    """

    def render(self) -> RenderableType:
        if self.any:
            return self._tree
        else:
            return Align.center(
                NO_MATCH, vertical="middle", height=round(get_terminal_size()[1] * 0.8)
            )

    def render_about(self, node, _) -> RenderableType:
        label: Text = super().render_about(node, _)
        if self.highlighted_node == node:
            label.append(" <=")

        if val := self.search.value:
            label.highlight_regex(val, style="red")

        return label

    async def set_values(self, nodes):
        """
        Initialize with all the values
        """

        self.all_nodes: dict[NodeID, TreeNode] = nodes
        self.search = SimpleInput()
        self.search.view = View(0, 100)
        self.search.on_focus()
        self.searching = True
        await self.refresh_search()

    async def refresh_search(self) -> None:
        """
        Refresh tree on search value change
        """

        self.any = False
        self.root.children = []

        for i in list(self.nodes.keys()):
            if i != self.root.id:
                self.nodes.pop(i)

        self.root.tree.children = []
        self.cursor_line = 0
        self.highlighted = self.root.id

        for id, i in self.all_nodes.items():
            if i.data.about.value and self.search.value in i.data.about.value:
                i.data.id = id
                await self.root.add("", i.data)
                self.any = True

        self.refresh(layout=True)

    async def find_id(self) -> NodeID:
        uuid = self.nodes[self.highlighted].data.uuid
        for id, i in self.all_nodes.items():
            if i.data.uuid == uuid:
                return id

        return NodeID(0)

    async def key_press(self, event: events.Key) -> None:
        if self.searching:
            match event.key:
                case "escape":
                    if self.searching:
                        self.searching = False
                        self.search.on_blur()
                        self.highlight(self.root.id)
                        await self.cursor_down()

                case _:
                    await self.search.handle_keypress(event.key)
                    await self.refresh_search()

        else:
            keys = self.keys
            match event.key:
                case i if i in keys.start_search:
                    self.searching = True
                    self.search.on_focus()
                case "escape":
                    await self.post_message(ChangeStatus(self, "NORMAL"))
                case i if i in keys.move_down:
                    await self.cursor_down()
                case i if i in keys.move_up:
                    await self.cursor_up()
                case i if i in keys.move_to_top:
                    await self.move_to_top()
                case i if i in keys.move_to_bottom:
                    await self.move_to_bottom()
                case "enter":
                    await self.post_message(ChangeStatus(self, "NORMAL"))
                    await self.post_message(HighlightNode(self, await self.find_id()))

        self.refresh()
