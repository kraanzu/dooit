from typing import Optional
from rich.console import RenderableType
from rich.text import Span, Text
from dooit.api.model import Model
from dooit.ui.widgets.base import HelperWidget


class SearchMenu(HelperWidget):
    _status = "SEARCH"

    def __init__(self, model: Model, children_type):
        super().__init__(id=f"SearchMenu-{model.uuid}")
        self.current = 0
        self.filter = []
        self.children_type = children_type
        self.model = model
        self.add_keys({"stop": "<enter>", "cancel": "<escape>"})

    @property
    def current_option(self) -> Optional[str]:
        if not self.visible_options:
            return

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

    async def stop(self) -> None:
        from dooit.ui.widgets.tree import Tree

        if self.current_option:
            query = (
                "WorkspaceTree"
                if self.children_type == "workspace"
                else "TodoTree.current"
            )
            tree = self.app.query_one(
                query,
                expect_type=Tree,
            )
            tree.current = tree.get_widget_by_id(self.current_option)

        await self.hide()
        self.apply_filter("")

    def render(self) -> RenderableType:
        res = Text()
        for index, (description, _) in enumerate(self.visible_options):
            if isinstance(self.filter, list):
                filter = " ".join(self.filter)
            else:
                filter = self.filter

            description = Text(description)
            plain = description.plain.lower()
            filter = filter.lower()

            if filter in plain:
                highlight_start = plain.index(filter)
                highlight_end = highlight_start + len(self.filter)
                span = Span(highlight_start, highlight_end, "red")
                description.spans.append(span)

            if index == self.current:
                pointer = Text("> ")
            else:
                pointer = Text("  ")

            res += pointer + description + Text("\n")

        return res
