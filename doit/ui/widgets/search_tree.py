from textual import events
from textual_extras.widgets.single_level_tree_edit import SimpleInput
from doit.ui.events.events import ChangeStatus, HighlightNode
from doit.ui.widgets.todo_list import TodoList
from textual.widgets import NodeID, TreeNode


class SearchTree(TodoList):
    async def set_values(self, nodes):
        self.all_nodes: dict[NodeID, TreeNode] = nodes
        self.search = SimpleInput()
        self.searching = True
        await self.refresh_search()

    async def refresh_search(self):
        self.root.children = []
        self.root.tree.children = []
        self.cursor_line = 0
        self.highlighted = self.root.id

        for id, i in self.all_nodes.items():
            if i.data.about.value and self.search.value in i.data.about.value:
                i.data.id = id
                await self.root.add("", i.data)

        self.refresh()

    async def find_id(self) -> NodeID:
        uuid = self.nodes[self.highlighted].data.uuid
        for id, i in self.all_nodes.items():
            if i.data.uuid == uuid:
                return id
        exit()

    async def key_press(self, event: events.Key):
        if self.searching:
            match event.key:
                case "escape":
                    if self.searching:
                        self.searching = False
                        if children := self.root.children:
                            self.highlighted = children[0].id

                case _:
                    await self.search.handle_keypress(event.key)
                    await self.refresh_search()

        else:
            match event.key:
                case "/":
                    self.searching = True
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
