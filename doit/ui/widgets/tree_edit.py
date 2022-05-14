from rich.console import RenderableType
from rich.text import Text
from textual import events
from textual.widgets import TreeControl, TreeNode, NodeID
from .entry import Entry


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
        self.selected = id
        self.refresh()

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
                case "z":
                    if self.highlighted:
                        await self.nodes[self.highlighted].toggle()

                case "j" | "down":
                    if self.highlighted:
                        self.highlighted = (
                            self.nodes[self.highlighted].next_node
                            or self.root.children[0]
                        ).id
                    else:
                        self.highlighted = self.root.children[0].id

                case "k" | "up":
                    if self.highlighted:
                        prev_node = self.nodes[self.highlighted].previous_node
                        if prev_node == self.root:
                            prev_node = self.root.children[-1]

                        # SAFETY: The node will never be None because it does not even reach root
                        self.highlighted = (prev_node).id
                    else:
                        self.highlighted = self.root.children[0].id
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
                str(node.data.render()).ljust(100, " "),
            )
        else:
            label = Text()

        if node.id != self.highlighted or self.hover_node:
            label.stylize("reverse green")
        elif not self.hover_node:
            label.stylize("reverse magenta")

        if node.id == self.hover_node or (
            not self.hover_node and self.highlighted == node.id
        ):
            label.stylize("reverse magenta")

        if node.id == self.selected:
            label.stylize("bold cyan")

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
            "cursor": node.is_cursor,
        }

        label.apply_meta(meta)
        return label


if __name__ == "__main__":

    from textual.app import App
    from textual.widgets import TreeClick

    class MyApp(App):
        async def on_mount(self):
            self.a = TreeEdit(Text("hi"))
            for i in range(10):
                await self.a.root.add(str(i), Entry("hi"))

            await self.a.root.children[0].add("x", Entry("hi"))
            await self.view.dock(self.a, edge="left", size=40)

        async def on_key(self, e):
            await self.a.handle_keypress(e)

        async def handle_tree_click(self, message: TreeClick):
            box = message.node.data
            if box:
                box._has_focus = True
                self.a.highlight(message.node.id)
                await self.a.select(message.node.id)

    MyApp.run()
