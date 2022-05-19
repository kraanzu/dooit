from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode

from ...ui.events import *
from ...ui.widgets import TreeEdit


class TodoList(TreeEdit):
    """
    A Class that allows editing while displaying trees
    """

    async def edit_current_node(self) -> None:
        await self.post_message(ChangeStatus(self, "INSERT"))
        return await super().edit_current_node()

    async def check_node(self):
        node = self.nodes[self.highlighted]
        if not str(node.data.render()).strip():
            await self.handle_keypress(events.Key(self, "x"))

    async def handle_key(self, key: str) -> None:
        match key:
            case "d":
                pass
            case "+" | "=":
                self.nodes[self.highlighted].data.increase_urgency()
            case "-" | "_":
                self.nodes[self.highlighted].data.decrease_urgency()

        await super().handle_key(key)

    async def handle_keypress(self, event: events.Key) -> None:
        if event.key == "escape":
            await self.post_message(ChangeStatus(self, "NORMAL"))
            if self.editing:
                await self.clear_select()
                await self.check_node()
            else:
                await self.post_message(Keystroke(self, event.key))
                await self.reset()

        elif not self.editing:
            await self.handle_key(event.key)
            if event.key != "i":
                await self.post_message(Keystroke(self, event.key))

        elif self.editing:
            await self.nodes[self.editing].data.handle_keypress(event.key)
            self.refresh()

    def render_node(self, node: TreeNode) -> RenderableType:
        """
        Renders styled node
        """

        # Setting up text
        if data := node.data:
            try:
                label = Text.from_markup(
                    str(data.render()),
                )
            except:
                label = Text(str(data.render()))
        else:
            label = Text()

        # setup milestone
        if children := node.children:
            total = len(children)
            done = sum(child.data.todo.status == "COMPLETE" for child in children)
            label.append(Text.from_markup(f" ( [green][/green] {done}/{total} )"))

        # fix padding
        label.plain = " " + label.plain
        label.pad_right(self.size.width, " ")

        # setup highlight
        if node.id == self.editing:
            label.stylize("bold reverse cyan")
        elif node.id == self.highlighted:
            label.stylize("bold reverse blue")

        # setup pre-icons
        if node != self.root:
            match node.data.todo.status:
                case "COMPLETE":
                    label = Text.from_markup(" [b green] [/b green]") + label
                case "PENDING":
                    label = Text.from_markup(" [b yellow] [/b yellow]") + label
                case "OVERDUE":
                    label = Text.from_markup(" [b yellow] [/b yellow]") + label

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)
        return label
