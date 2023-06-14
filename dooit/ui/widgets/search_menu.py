from typing import Optional, Union
from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget
from dooit.api.workspace import Workspace
from dooit.api.todo import Todo
from dooit.ui.events.events import StopSearch
from dooit.utils.keybinder import KeyBinder, KeyList


class SearchMenu(Widget):
    key_manager = KeyBinder()

    def __init__(self, model: Union[Todo, Workspace], children_type):
        super().__init__(classes="focus")
        self.add_keys()
        self.border_title = f"search {children_type}s"
        self.current = -1
        self.filter = []
        self.children_type = children_type

        if children_type == "workspace":
            options = model.get_workspaces()
        else:
            options = model.get_todos()

        self.options = [(i.description, i.uuid) for i in options]
        self.visible_options = self.options[:]

    def add_keys(self):
        additional_keys: KeyList = {
            "signal_stop_search": "<escape>",
            "signal_goto_item": "<enter>",
        }
        self.key_manager.add_keys(additional_keys)

    async def move_down(self):
        self.current = min(self.current + 1, len(self.visible_options) - 1)

    async def move_up(self):
        self.current = max(self.current - 1, 0)

    async def signal_stop_search(self):
        self.post_message(StopSearch())

    async def signal_goto_item(self):
        if self.current != -1:
            self.post_message(StopSearch(self.visible_options[self.current][1]))
        else:
            await self.signal_stop_search()

    async def keypress(self, key):
        self.key_manager.attach_key(key)
        bind = self.key_manager.get_method()
        if bind:
            if hasattr(self, bind.func_name):
                func = getattr(self, bind.func_name)
                await func(*bind.params)
        self.refresh()

    def reset_cursor(self):
        self.current = -1

    def apply_filter(self, words: str):
        self.visible_options = [
            (description, uuid)
            for description, uuid in self.options
            if all(word in description.lower() for word in words.lower().split())
        ]
        self.filter = words
        self.reset_cursor()
        self.refresh()

    def stop_search(self, id_: Optional[str] = None):
        from dooit.ui.widgets.todo_tree import TodoTree
        from dooit.ui.widgets.workspace_tree import WorkspaceTree

        if self.children_type == "workspace":
            w = WorkspaceTree
            w = self.app.query_one(w)
        else:
            w = TodoTree
            w = [i for i in self.app.query(w) if i.has_class("current")][0]

        with self.app.batch_update():
            if id_:
                w.current = id_

            w.display = True
            self.remove()

    def render(self) -> RenderableType:
        res = Text()
        for index, (description, _) in enumerate(self.visible_options):
            description = Text(description)
            description.highlight_words(
                self.filter,
                "red",
                case_sensitive=False,
            )
            if index == self.current:
                pointer = Text("> ")
            else:
                pointer = Text("  ")

            res += pointer + description + Text("\n")

        return res
