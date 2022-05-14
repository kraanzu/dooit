from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeControl, TreeNode, NodeID
from textual.events import Key


class TreeEdit(TreeControl):
    """
    A Class that allows editing while displaying trees
    """

    def __init__(self, label: Text) -> None:
        super().__init__(label, None)
        self._tree.hide_root = True
        self.root._tree.expanded = True

        self.highlighted = None
        self.selected = None

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        self.highlighted = event.style.meta.get("tree_node")
        return await super().on_mouse_move(event)

    async def reset(self) -> None:
        """
        Turns off both highlight and editing
        """
        await self.clear_select()
        self.highlighted = None

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

    async def handle_click(self) -> None:
        # Yeah I know this is weird. BUT IT WORKS DAMMIT!
        await self.handle_keypress(Key(self, "enter"))

    def highlight(self, id: NodeID | None = None) -> None:
        """
        Highlights the node
        """

        self.highlighted = id
        self.refresh()

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
            match event.key:
                case "enter":
                    await self.select(self.highlighted)
                case "z":
                    if self.highlighted:
                        await self.nodes[self.highlighted].toggle()

                case "j" | "down":
                    if self.highlighted:
                        self.highlight(
                            (
                                self.nodes[self.highlighted].next_node
                                or self.root.children[0]
                            ).id
                        )
                    else:
                        self.highlight(self.root.children[0].id)

                case "k" | "up":
                    if self.highlighted:
                        prev_node = self.nodes[self.highlighted].previous_node
                        if prev_node == self.root:
                            prev_node = self.root.children[-1]

                        # SAFETY: The node will never be None because it does not even reach root
                        self.highlight(prev_node.id)
                    else:
                        self.highlight(self.root.children[0].id)
        else:
            if self.selected:
                await self.nodes[self.selected].data.handle_keypress(event.key)

        self.refresh(layout=True)

    def render_node(self, node: TreeNode) -> RenderableType:
        """
        Renders styled node
        """

        if node.data:
            label = Text(
                str(node.data.render()),
            )
        else:
            label = Text()

        # WASTE
        if self.hover_node:
            label = Text("Hover ") + label
        if self.highlighted:
            label = Text(f"high({self.highlighted}) ") + label
        #######

        if node.id == self.selected:
            label.stylize("cyan")
        elif node.id == self.highlighted:
            label.stylize("magenta")
        else:
            label.stylize("yellow")

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)
        return label
