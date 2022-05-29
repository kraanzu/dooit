import datetime
from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode
from textual_extras.widgets import NestedListEdit

from doit.ui.widgets.todo_list import TodoList

from ...ui.events.events import PostMessage


class DateTree(TodoList):
    async def validate(self, day, month, year) -> bool:
        try:
            datetime.datetime(int(year), int(month), int(day))
            return True
        except ValueError:
            return False

    async def add_child(self):
        node = self.nodes[self.highlighted]
        if node == self.root or node.parent == self.root:
            await node.add("child", self.get_box())
            await node.expand()
            await self.reach_to_last_child()

    async def add_sibling(self):
        if self.nodes[self.highlighted].parent == self.root:
            await self.root.add("child", self.get_box())
            await self.move_to_bottom()
        else:
            await self.reach_to_parent()
            await self.add_child()

    async def on_key(self, event: events.Key) -> None:
        if event.key == "i":
            return
        elif event.key == "d":
            await self.focus_node()

        await super().on_key(event)

    def render_custom_node(self, node: TreeNode) -> RenderableType:

        color = "yellow"

        # setup text
        if data := node.data:
            label = Text(str(data.todo.due))
            match node.data.todo.due:
                case "COMPLETE":
                    color = "green"

                case "OVERDUE":
                    color = "red"
        else:
            label = Text()

        if not label.plain:
            label = Text("No due date")

        # fix padding
        label = Text(" ") + label
        label.plain += " " * (13 - len(label.plain))
        if node.id == self.highlighted:
            style = "yellow" if self.editing else "blue"
            label.stylize(f"bold reverse {style}")

        # setup pre-icons
        label = Text.from_markup(f"[{color}]   [/{color}]") + label

        return label
