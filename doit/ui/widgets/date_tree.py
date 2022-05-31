from datetime import datetime
import re
from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeNode

from ...ui.widgets import TodoList
from ...ui.events.events import ChangeStatus, ModifyDue, Statusmessage


class DateTree(TodoList):
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

    async def focus_node(self) -> None:
        if self.highlighted == self.root.id:
            return

        self.prev_value = self.nodes[self.highlighted].data.value
        self.nodes[self.highlighted].data.on_focus()
        self.editing = True
        await self.post_message(ChangeStatus(self, "DATE"))

    async def unfocus_node(self) -> None:
        self.nodes[self.highlighted].data.on_blur()
        self.editing = False
        await self.post_message(ChangeStatus(self, "NORMAL"))

    async def key_press(self, event: events.Key) -> None:
        if self.editing:
            match event.key:
                case "escape":
                    await self.unfocus_node()
                    await self.check_node()
                case _:
                    await super().send_key_to_selected(event)

        else:
            match event.key:
                case "j" | "down":
                    await self.cursor_down()
                case "k" | "up":
                    await self.cursor_up()
                case "g":
                    await self.move_to_top()
                case "G":
                    await self.move_to_bottom()
                case "z":
                    await self.toggle_expand()
                case "Z":
                    await self.toggle_expand_parent()
                case "A":
                    await self.add_child()
                case "a":
                    await self.add_sibling()
                case "d":
                    await self.focus_node()
                case "x":
                    await self.remove_node()

        self.refresh()

    def _parse_date(self, date: str) -> tuple:
        day = int(date[:2])
        month = int(date[3:5])
        year = int(date[6:])

        return year, month, day

    def _is_valid_date(self, date: str) -> bool:
        try:
            datetime(*self._parse_date(date))
            return True
        except ValueError:
            return False

    def _is_expired(self, date):
        present = datetime.now()
        due = datetime(*self._parse_date(date))

        return due < present

    async def update_due_status(self, date):
        status = self.nodes[self.highlighted].data.todo.status
        if status == "COMPLETED":
            return

        if self._is_expired(date):
            await self.post_message(ModifyDue(self, status="OVERDUE"))
        else:
            await self.post_message(ModifyDue(self, status="PENDING"))

    async def check_node(self):
        date = self.nodes[self.highlighted].data.value

        if len(date) == 10 and re.findall("^\d\d-\d\d-\d\d\d\d$", date):
            if not self._is_valid_date(date):
                await self.post_message(
                    Statusmessage(self, message="Please enter a valid date")
                )
            else:
                await self.post_message(
                    Statusmessage(self, message="You due date was updated")
                )
                await self.update_due_status(date)
                return

        else:
            await self.post_message(
                Statusmessage(
                    self, message="Invalid date format! Enter in format: dd-mm-yyyy"
                )
            )

        self.nodes[self.highlighted].data.value = self.prev_value
        self.refresh()

    def render_custom_node(self, node: TreeNode) -> RenderableType:

        match node.data.todo.status:
            case "PENDING":
                color = "yellow"
            case "COMPLETED":
                color = "green"
            case "OVERDUE":
                color = "red"

        # Setting up text
        label = Text.from_markup(
            str(node.data.render()),
        )

        if not label.plain:
            label = Text("Until You Die")

        # fix padding
        label.pad_right(self.size.width)

        if node.id == self.highlighted:
            if self.editing:
                label.stylize(self.style_editing)
            else:
                label.stylize(self.style_focus)
        else:
            label.stylize(self.style_unfocus)

        label = label[:13]

        # SAFETY: color will never be unbound
        # because the match statement in exhaustive
        if color == "green":
            label.stylize("strike")

        label = Text.from_markup(f"[{color}]  [/{color}]") + label

        return label
