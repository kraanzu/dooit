from rich.console import RenderableType
from rich.padding import PaddingDimensions
from rich.style import StyleType
from rich.text import Text, TextType
from textual import events
from textual.widgets import TreeControl, TreeNode, NodeID
from textual.messages import CursorMove

from ...ui.widgets.simple_input import SimpleInput, View


class NestedListEdit(TreeControl):
    """
    A editable & nested list
    """

    def __init__(
        self,
        label: TextType,
        data: RenderableType = SimpleInput(),
        name: str | None = None,
        padding: PaddingDimensions = (1, 1),
        style_unfocus: StyleType = "d white",
        style_focus: StyleType = "b blue",
        style_editing: StyleType = "b cyan",
    ) -> None:
        super().__init__(label, data, name=name, padding=padding)
        self._tree.hide_root = True
        self._tree.expanded = True
        self.style_focus = style_focus
        self.style_unfocus = style_unfocus
        self.style_editing = style_editing
        self.editing = False
        self.highlight(self.root.id)

        from ...utils import conf

        self.keys = conf.keys

    async def watch_cursor_line(self, value: int) -> None:
        await self.post_message(CursorMove(self, value + self.gutter.top))

    def highlight(self, id: NodeID) -> None:
        self.highlighted = id
        self.highlighted_node = self.nodes[self.highlighted]
        self.refresh()

    async def focus_node(self, part: str = "about") -> None:
        await self.highlighted_node.data.make_focus(part)
        self.editing = True

    async def unfocus_node(self) -> None:
        await self.highlighted_node.data.remove_focus()
        self.editing = False

    async def remove_node(self, id: NodeID | None = None) -> None:
        if id == self.root.id:
            return

        node = self.nodes[id or self.highlighted]

        if node.expanded:
            await node.toggle()

        if node.next_node:
            await self.cursor_down()
        elif prev_node := node.previous_node:
            if prev_node == self.root:
                self.highlight(self.root.id)
            else:
                await self.cursor_up()

        parent = node.parent or self.root
        for index, child in enumerate(parent.children):
            if child == node:
                parent.children.pop(index)
                parent.tree.children.pop(index)
                del self.nodes[node.id]

        self.refresh(layout=True)

    async def key_down(self, _: events.Key) -> None:
        pass

    async def key_up(self, _: events.Key) -> None:
        pass

    async def cursor_down(self) -> None:
        node = self.highlighted_node

        if next_node := node.next_node:
            self.cursor_line += 1
            self.highlight(next_node.id)
        elif node == self.root:
            if node.children:
                self.cursor_line += 1
                self.highlight(node.children[0].id)

    async def cursor_up(self) -> None:
        node = self.highlighted_node

        if prev_node := node.previous_node:
            if prev_node != self.root:
                self.cursor_line -= 1
                self.highlight(prev_node.id)

    async def shift_up(self):
        if prev := self.highlighted_node.previous_node:
            if prev != self.highlighted_node.parent:
                parent = self.highlighted_node.parent or self.root
                children = parent.children
                tree = parent.tree.children
                pos = children.index(self.highlighted_node)
                children[pos], children[pos - 1] = children[pos - 1], children[pos]
                tree[pos], tree[pos - 1] = tree[pos - 1], tree[pos]

    async def shift_down(self):
        if node := self.highlighted_node.next_node:
            if node.parent == self.highlighted_node.parent:
                parent = self.highlighted_node.parent or self.root
                children = parent.children
                tree = parent.tree.children
                pos = children.index(self.highlighted_node)
                children[pos], children[pos + 1] = children[pos + 1], children[pos]
                tree[pos], tree[pos + 1] = tree[pos + 1], tree[pos]

    async def move_to_top(self) -> None:
        if children := self.root.children:
            self.highlight(children[0].id)
            self.cursor_line = 0

    async def move_to_bottom(self) -> None:
        if children := self.root.children:
            while self.highlighted != children[-1].id:
                await self.cursor_down()

    async def toggle_expand(self) -> None:
        if self.highlighted != self.root.id:
            await self.highlighted_node.toggle()

    async def toggle_expand_parent(self) -> None:
        if (
            self.highlighted != self.root.id
            and self.highlighted_node.parent != self.root
        ):
            await self.reach_to_parent()
            await self.highlighted_node.toggle()

    async def reach_to_parent(self) -> None:
        node = self.highlighted_node
        if parent := node.parent:
            index = parent.children.index(node) + 1
            self.cursor_line -= index
            self.highlight(parent.id)

    async def reach_to_last_child(self) -> None:
        if children := self.highlighted_node.children:
            self.cursor_line += len(children)
            self.highlight(children[-1].id)

    async def add_child(self) -> None:
        node = self.highlighted_node
        await node.add("child", SimpleInput())
        await node.expand()
        await self.reach_to_last_child()
        await self.focus_node()

    async def add_sibling(self) -> None:
        if self.highlighted_node.parent == self.root:
            await self.root.add("child", SimpleInput())
            await self.move_to_bottom()
        else:
            await self.reach_to_parent()
            await self.add_child()
        await self.focus_node()

    async def send_key_to_selected(self, event: events.Key) -> None:
        await self.highlighted_node.data.send_key(event)

    async def key_press(self, event: events.Key):
        if self.editing:
            match event.key:
                case "escape":
                    await self.unfocus_node()
                case "enter":
                    if self.highlighted_node.data.value:
                        await self.unfocus_node()
                        if not self.editing:
                            await self.add_sibling()
                case _:
                    await self.send_key_to_selected(event)

        else:
            keys = self.keys
            match event.key:
                case i if i in keys.move_down:
                    await self.cursor_down()
                case i if i in keys.shift_down:
                    await self.shift_down()
                case i if i in keys.move_up:
                    await self.cursor_up()
                case i if i in keys.shift_up:
                    await self.shift_up()
                case i if i in keys.move_to_top:
                    await self.move_to_top()
                case i if i in keys.move_to_bottom:
                    await self.move_to_bottom()
                case i if i in keys.toggle_expand:
                    await self.toggle_expand()
                case i if i in keys.toggle_expand_parent:
                    await self.toggle_expand_parent()
                case i if i in keys.add_child:
                    await self.add_child()
                case i if i in keys.add_sibling:
                    await self.add_sibling()
                case i if i in keys.edit_node:
                    if self.highlighted != self.root.id:
                        await self.focus_node()
                case i if i in keys.remove_node:
                    if self.highlighted != self.root.id:
                        await self.remove_node()

        self.refresh()

    async def on_mouse_move(self, event: events.MouseMove) -> None:
        """
        Move the highlight along with mouse hover
        """

        if not self.editing:
            if id := event.style.meta.get("tree_node"):
                self.highlight(id)

    def render_node(self, node: TreeNode) -> RenderableType:

        if not hasattr(node.data.about, "view"):
            node.data.about.view = View(0, self.size.width - 6)

        return self.render_custom_node(node)

    def render_custom_node(self, node) -> Text:

        label = (
            Text(str(node.data.about.render()), no_wrap=True)
            if isinstance(node.label, str)
            else node.label
        )
        label.pad_right(self.size.width)

        if node.id == self.highlighted:
            label.stylize(self.style_focus)
        else:
            label.stylize(self.style_unfocus)

        meta = {
            "@click": f"click_label({node.id})",
            "tree_node": node.id,
        }

        label.apply_meta(meta)
        return label

    async def handle_tree_click(self, *_) -> None:
        if not self.editing:
            await self.focus_node()
            self.refresh()
