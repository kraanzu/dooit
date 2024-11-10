from typing import TYPE_CHECKING, Optional

from textual.widgets import ContentSwitcher

from dooit.api import Workspace
from dooit.api.theme import DooitThemeBase
from dooit.api.todo import Todo
from dooit.ui.widgets.trees import WorkspacesTree, TodosTree
from ._base import ApiComponent


if TYPE_CHECKING:  # pragma: no cover
    from dooit.ui.tui import Dooit


class VarManager(ApiComponent):
    def __init__(self, app: "Dooit") -> None:
        super().__init__()
        self.app = app
        self._show_confirm = True

    @property
    def show_confirm(self):
        return self._show_confirm

    @show_confirm.setter
    def show_confirm(self, value: bool):
        self._show_confirm = value

    @property
    def mode(self) -> str:
        return self.app.current_mode

    @property
    def theme(self) -> DooitThemeBase:
        return self.app.current_theme

    @property
    def workspaces_tree(self) -> WorkspacesTree:
        return self.app.query_one(WorkspacesTree)

    @property
    def current_workspace(self) -> Optional[Workspace]:
        tree = self.app.workspace_tree
        if tree.highlighted is None:
            return None

        return tree.current_model

    @property
    def todos_tree(self) -> Optional[TodosTree]:
        todo_switcher = self.app.query_one(
            "#todo_switcher", expect_type=ContentSwitcher
        )
        if todo_switcher.visible_content and isinstance(
            todo_switcher.visible_content, TodosTree
        ):
            return todo_switcher.visible_content

    @property
    def current_todo(self) -> Optional[Todo]:
        tree = self.todos_tree
        if tree is None:
            return

        if tree.highlighted is None:
            return

        todo = tree.current_model
        assert isinstance(todo, Todo)

        return todo
