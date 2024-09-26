from textual.app import App
from dooit.ui.api.widgets import TodoLayout, WorkspaceLayout
from dooit.ui.widgets.trees import TodosTree, WorkspacesTree
from ._base import ApiComponent


class LayoutManager(ApiComponent):
    def __init__(self, app: App) -> None:
        self.app = app
        self._todo_layout: TodoLayout = []
        self._workspace_layout: WorkspaceLayout = []

    @property
    def todo_layout(self) -> TodoLayout:
        return self._todo_layout

    @todo_layout.setter
    def todo_layout(self, layout: TodoLayout):
        self._todo_layout = layout
        for tree in self.app.query(TodosTree):
            tree.refresh_options()

    @property
    def workspace_layout(self) -> WorkspaceLayout:
        return self._workspace_layout

    @workspace_layout.setter
    def workspace_layout(self, layout: WorkspaceLayout):
        self._workspace_layout = layout
        for tree in self.app.query(WorkspacesTree):
            tree.refresh_options()
