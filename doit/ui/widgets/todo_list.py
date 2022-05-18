from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode

from doit.ui.events import *
from ...ui.widgets.tree_edit import TreeEdit


class TodoList(TreeEdit):
    """
    A Class that allows editing while displaying trees
    """

    async def handle_keypress(self, event: events.Key) -> None:
        if event.key == "escape":
            if self.editing:
                await self.clear_select()
            else:
                await self.post_message(Keystroke(self, event.key))
                await self.reset()

        elif not self.editing:
            await self.handle_shortcut(event.key)
            if event.key != "i":
                await self.post_message(Keystroke(self, event.key))

        elif self.editing:
            await self.nodes[self.editing].data.handle_keypress(event.key)
            self.refresh()

    def render_node(self, node: TreeNode) -> RenderableType:
        """
        Renders styled node
        """

        if data := node.data:
            try:
                label = Text.from_markup(
                    str(data.render()),
                )
            except:
                label = Text(str(data.render()))
        else:
            label = Text()

        if node.id == self.editing:
            label = Text(" ") + label + " "
            label.stylize("bold reverse cyan")
        elif node.id == self.highlighted:
            label = Text(" ") + label + " "
            label.stylize("bold reverse blue")

        if node != self.root:
            match node.data.todo.status:
                case "COMPLETE":
                    label = Text.from_markup("[b green] [/b green]") + label
                case "PENDING":
                    label = Text.from_markup("[b yellow] [/b yellow]") + label
                case "OVERDUE":
                    label = Text.from_markup("[b yellow] [/b yellow]") + label

        if children := node.children:
            total = len(children)
            done = sum(child.data.todo.status == "COMPLETE" for child in children)
            label.append(Text.from_markup(f" ( [green][/green] {done}/{total} )"))

        label = Text(" ") + label

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)
        return label
