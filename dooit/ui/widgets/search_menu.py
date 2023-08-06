from typing import Optional
from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget
from dooit.api.model import Model
from dooit.ui.widgets.kwidget import KeyWidget


class SearchMenu(KeyWidget, Widget):
    def __init__(self, model: Model, children_type):
        super().__init__()
        self.current = -1
        self.filter = []
        self.children_type = children_type

        if children_type == "workspace":
            options = model.get_workspaces()
        else:
            options = model.get_todos()

        self.options = [(i.description, i.uuid) for i in options]
        self.visible_options = self.options[:]
        self.add_keys({"stop_search": "<enter>", "cancel_search": "<escape>"})

    @property
    def current_option(self) -> Optional[str]:
        if self.current:
            return self.visible_options[self.current][1]

    async def move_down(self):
        self.current = min(self.current + 1, len(self.visible_options) - 1)

    async def move_up(self):
        self.current = max(self.current - 1, 0)

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

    async def cancel_search(self):
        if self.parent:
            await self.parent.stop_search()

        self.remove()

    async def stop_search(self):
        from dooit.ui.widgets.tree import Tree

        if self.parent and self.current_option:
            parent = self.app.query_one(f"#{self.parent.id}", expect_type=Tree)
            await parent.stop_search(self.current_option)

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
