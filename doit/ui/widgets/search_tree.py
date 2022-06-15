from os import get_terminal_size
from rich.align import Align
from rich.console import RenderableType
from textual import events
from doit.ui.events.events import ChangeStatus, HighlightNode
from doit.ui.widgets.simple_input import SimpleInput, View
from doit.ui.widgets.todo_list import TodoList
from textual.widgets import NodeID, TreeNode

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
            return super().render()
        else:
            return Align.center(
                NO_MATCH, vertical="middle", height=round(get_terminal_size()[1] * 0.8)
            )

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
            match event.key:
                case "/":
                    self.searching = True
                    self.search.on_focus()
                case "escape":
                    await self.post_message(ChangeStatus(self, "NORMAL"))
                case "j" | "down":
                    await self.cursor_down()
                case "k" | "up":
                    await self.cursor_up()
                case "g":
                    await self.move_to_top()
                case "G":
                    await self.move_to_bottom()
                case "enter":
                    await self.post_message(ChangeStatus(self, "NORMAL"))
                    await self.post_message(HighlightNode(self, await self.find_id()))

        self.refresh()
