from typing import Optional
from rich.console import RenderableType
from rich.text import Text
from textual.widget import Widget
from dooit.api.model import Model
from dooit.ui.widgets.base import KeyWidget


class SearchMenu(KeyWidget, Widget):
    DEFAULT_CSS = """
    SearchMenu {
        layer: L1;
        display: none;
    }
    """

    def __init__(self, model: Model, children_type):
        super().__init__(id=f"SearchMenu-{model.uuid}")
        self.current = 0
        self.filter = []
        self.children_type = children_type
        self.model = model
        self.add_keys({"stop_search": "<enter>", "cancel_search": "<escape>"})

    @property
    def current_option(self) -> Optional[str]:
        return self.visible_options[self.current][1]

    def refresh_options(self) -> None:
        self.filter = []
        if self.children_type == "workspace":
            options = self.model.get_all_workspaces()
        else:
            options = self.model.get_all_todos()

        self.options = [(i.description, i.uuid) for i in options]
        self.visible_options = self.options[:]

    async def move_down(self) -> None:
        self.current = min(self.current + 1, len(self.visible_options) - 1)

    async def move_up(self) -> None:
        self.current = max(self.current - 1, 0)

    async def keypress(self, key) -> None:
        self.key_manager.attach_key(key)
        bind = self.key_manager.get_method()
        if bind:
            if hasattr(self, bind.func_name):
                func = getattr(self, bind.func_name)
                await func(*bind.params)
        self.refresh()

    def reset_cursor(self) -> None:
        self.current = 0

    def apply_filter(self, words: str) -> None:
        self.visible_options = [
            (description, uuid)
            for description, uuid in self.options
            if all(word in description.lower() for word in words.lower().split())
        ]
        self.filter = words
        self.reset_cursor()
        self.refresh()

    def hide(self) -> None:
        self.styles.layer = "L1"
        self.display = False

    async def start_search(self) -> None:
        self.styles.layer = "L4"
        self.display = True
        self.apply_filter("")

    async def cancel_search(self) -> None:
        self.hide()

    async def stop_search(self) -> None:
        from dooit.ui.widgets.tree import Tree

        if self.current_option:
            query = (
                "WorkspaceTree"
                if self.children_type == "workspace"
                else "TodoTree.current"
            )
            self.app.query_one(
                query,
                expect_type=Tree,
            ).current = self.current_option

        self.hide()

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
