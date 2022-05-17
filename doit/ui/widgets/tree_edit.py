from typing import Literal
from rich.console import RenderableType
from rich.text import TextType, Text
from textual import events
from textual.widgets import TreeControl, NodeID, TreeNode
from textual.events import Key
from textual.messages import CursorMove

from ...ui.widgets.entry import Entry


class TreeEdit(TreeControl):
    """
    A Class that allows editing while displaying trees
    """

    def __init__(self, label: TextType = "", data: Entry = Entry()) -> None:
        super().__init__(label, data)
        self._tree.hide_root = True
        self.root._tree.expanded = True

        self.current_line = 0
        self.highlighted = NodeID(0)
        self.selected = None

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        self.highlighted = event.style.meta.get("tree_node")
        return await super().on_mouse_move(event)

    async def reset(self) -> None:
        """
        Turns off both highlight and editing
        """
        await self.clear_select()
        self.highlighted = NodeID(0)

    async def move_cursor_line(self, delta: int = 0, pos: int = 0) -> None:
        if delta:
            self.current_line += delta
        else:
            self.current_line = pos
        self.emit_no_wait(CursorMove(self, self.current_line))

    async def clear_select(self) -> None:
        """
        Leave editing mode
        """

        if self.selected:
            self.nodes[self.selected].data._has_focus = False

        self.selected = None
        self.refresh()

    async def select(self, id: NodeID | None = None) -> None:
        """
        Selects the node to be edited
        """
        await self.clear_select()
        self.highlighted = id
        self.selected = id
        if self.selected:
            self.nodes[self.selected].data._has_focus = True

        self.hover_node = None  # Not to block due to still mouse pointer
        self.refresh()

    async def remove(self, id: NodeID):
        if self.nodes[id].next_node:
            await self.move_highlight_down()
        elif self.nodes[id].previous_node:
            await self.move_highlight_up()

        parent = self.nodes[id].parent or self.root
        for index, child in enumerate(parent.children):
            if child.id == id:
                parent.children.pop(index)
                parent.tree.children.pop(index)

        self.refresh()

    async def handle_click(self) -> None:
        # Yeah I know this is weird. BUT IT WORKS DAMMIT!
        await self.handle_keypress(Key(self, "enter"))

    async def move_highlight_down(self):
        node = self.nodes[self.highlighted]
        if next_node := node.next_node:
            self.highlight(next_node.id)
            await self.move_cursor_line(delta=1)
        elif node == self.root and self.root.children:
            self.highlight(self.root.children[0].id)

    async def move_highlight_up(self):
        prev_node = self.nodes[self.highlighted].previous_node
        if prev_node and prev_node != self.root:
            self.highlight(prev_node.id)
            await self.move_cursor_line(delta=-1)

    def highlight(self, id: NodeID = NodeID(0)) -> None:
        """
        Highlights the node
        """

        self.highlighted = id
        self.refresh()

    async def handle_shortcut(self, key: str):
        async def reach_to_node(node: TreeNode, direction: Literal["up", "down"]):
            while self.highlighted != node.id:
                await self.handle_shortcut(direction)

        match key:
            case "g":
                while self.highlighted != self.root.children[0].id:
                    await self.handle_shortcut("k")

            case "G":
                while self.highlighted != self.root.children[-1].id:
                    await self.handle_shortcut("j")

            case "i":
                await self.select(self.highlighted)

            case "a":
                node = self.nodes[self.highlighted]
                await node.add("", Entry())
                await node.expand()
                await reach_to_node(node.children[-1], "down")
                await self.handle_shortcut("i")

            case "A":
                node = self.nodes[self.highlighted]
                if node.parent == self.root:
                    await self.root.add("", Entry())
                    await self.handle_shortcut("G")
                    await self.handle_shortcut("i")
                else:
                    # SAFETY: root parent case has already been handled above
                    await reach_to_node(node.parent, "up")
                    await self.handle_shortcut("a")

            case "c":
                self.nodes[self.highlighted].data.mark_complete()

            case "x":
                await self.remove(self.highlighted)

            case "z":
                if self.highlighted:
                    node = self.nodes[self.highlighted]
                    await node.toggle()

            case "Z":
                if parent := self.nodes[self.highlighted].parent:
                    if parent != self.root:
                        while self.nodes[self.highlighted].previous_node != parent:
                            await self.handle_shortcut("k")

                        await self.handle_shortcut("k")
                        await self.handle_shortcut("z")

            case "j" | "down":
                await self.move_highlight_down()

            case "k" | "up":
                await self.move_highlight_up()

    async def handle_keypress(self, event: events.Key) -> None:
        """
        Handle incoming kepresses
        """

        if event.key == "escape":
            if self.selected:
                await self.clear_select()
            else:
                await self.reset()

        elif not self.selected:
            await self.handle_shortcut(event.key)
        else:
            if self.selected:
                await self.nodes[self.selected].data.handle_keypress(event.key)

        self.refresh(layout=True)
