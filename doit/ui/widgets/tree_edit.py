from typing import Literal
from rich.text import TextType
from textual.widgets import TreeControl, NodeID, TreeNode
from textual.events import Key, MouseMove
from textual.messages import CursorMove

from ...ui.widgets.entry import Entry


class TreeEdit(TreeControl):
    """
    A Class that allows editing while displaying trees
    """

    def __init__(self, label: TextType = "", data: Entry = Entry()) -> None:
        super().__init__(label, data)
        self._tree.hide_root = True
        self._tree.guide_style = "conceal"
        self.root._tree.expanded = True

        self.current_line = 0
        self.highlighted = NodeID(0)
        self.editing = None

    async def on_mouse_move(self, event: MouseMove) -> None:
        """
        Highlights the node under cursor
        """

        self.highlighted = event.style.meta.get("tree_node")
        return await super().on_mouse_move(event)

    async def reset(self) -> None:
        """
        Turns off both highlight and editing
        """

        await self.clear_select()
        self.highlighted = NodeID(0)

    async def move_cursor_line(self, delta: int = 0, pos: int = 0) -> None:
        """
        Moves the cursor for scrollable view
        """
        if delta:
            self.current_line += delta
        else:
            self.current_line = pos
        self.emit_no_wait(CursorMove(self, self.current_line))

    async def clear_select(self) -> None:
        """
        Leave editing mode
        """

        if self.editing:
            self.nodes[self.editing].data._has_focus = False

        self.editing = None
        self.refresh()

    async def select(self, id: NodeID | None = None) -> None:
        """
        Selects the node to be edited
        """

        await self.clear_select()
        self.highlighted = id
        self.editing = id
        if self.editing:
            self.nodes[self.editing].data._has_focus = True

        self.hover_node = None  # Not to block due to still mouse pointer
        self.refresh()

    async def remove_node(self, id: NodeID | None) -> None:
        """
        Removes the specified node
        removes highlighted node by default
        """

        if id:
            node = self.nodes[id]
        else:
            node = self.nodes[self.highlighted]

        if node.expanded:
            await node.toggle()

        if node.next_node:
            await self.move_highlight_down()
        elif prev_node := node.previous_node:
            if prev_node == self.root:
                await self.reset()
            else:
                await self.move_highlight_up()

        parent = node.parent or self.root
        for index, child in enumerate(parent.children):
            if child.id == id:
                parent.children.pop(index)
                parent.tree.children.pop(index)

        self.refresh()

    async def handle_click(self) -> None:
        # Yeah I know this is weird. BUT IT WORKS DAMMIT!
        await self.handle_keypress(Key(self, "enter"))

    async def move_highlight_down(self) -> None:
        node = self.nodes[self.highlighted]
        if next_node := node.next_node:
            self.highlight(next_node.id)
            await self.move_cursor_line(delta=1)
        elif node == self.root and self.root.children:
            self.highlight(self.root.children[0].id)

    async def move_highlight_up(self) -> None:
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

    async def reach_to_node(
        self, node: TreeNode | None, direction: Literal["up", "down"]
    ) -> None:
        node = node or self.root
        while self.highlighted != node.id:
            await self.handle_key(direction)

    async def move_to_top(self) -> None:
        """
        Takes highlight to the top of the tree
        """

        while self.highlighted != self.root.children[0].id:
            await self.move_highlight_up()

    async def move_to_bottom(self) -> None:
        """
        Takes highlight to the top of the tree
        """

        while self.highlighted != self.root.children[-1].id:
            await self.move_highlight_down()

    async def edit_current_node(self):
        await self.select(self.highlighted)

    async def add_to_current_parent(self):
        """
        Adds node in the same indent
        """

        node = self.nodes[self.highlighted]
        await node.add("", Entry())
        await node.expand()
        await self.reach_to_node(node.children[-1], "down")
        await self.edit_current_node()

    async def add_child(self):
        """
        Adds a child node to current highlighted node
        """

        node = self.nodes[self.highlighted]
        if node.parent == self.root:
            await self.root.add("", Entry())
            await self.move_to_bottom()
            await self.edit_current_node()
        else:
            # SAFETY: root parent case has already been handled above
            await self.reach_to_node(node.parent, "up")
            await self.handle_key("A")

    async def toggle_current_node(self) -> None:
        """
        Toggles between expansion of node
        """

        if self.highlighted:
            node = self.nodes[self.highlighted]
            await node.toggle()

    async def toggle_current_parent(self) -> None:
        """
        Toggles between expansion of parent node
        """

        if parent := self.nodes[self.highlighted].parent:
            if parent != self.root:
                while self.nodes[self.highlighted].previous_node != parent:
                    await self.handle_key("k")

                await self.handle_key("k")
                await self.handle_key("z")

    async def handle_key(self, key: str) -> None:
        match key:
            case "g":
                await self.move_to_top()

            case "G":
                await self.move_to_bottom()

            case "i":
                await self.edit_current_node()

            case "A":
                await self.add_to_current_parent()

            case "a":
                await self.add_child()

            case "c":
                self.nodes[self.highlighted].data.mark_complete()

            case "x":
                await self.remove_node(self.highlighted)

            case "z":
                await self.toggle_current_node()

            case "Z":
                await self.toggle_current_parent()

            case "j" | "down":
                await self.move_highlight_down()

            case "k" | "up":
                await self.move_highlight_up()

    async def handle_keypress(self, event: Key) -> None:
        """
        Handle incoming kepresses
        """

        if event.key == "escape":
            if self.editing:
                await self.clear_select()
            else:
                await self.reset()

        elif not self.editing:
            await self.handle_key(event.key)
        else:
            if self.editing:
                await self.nodes[self.editing].data.handle_keypress(event.key)

        self.refresh(layout=True)
