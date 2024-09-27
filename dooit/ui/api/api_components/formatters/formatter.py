from textual.app import App
from .._base import ApiComponent
from .model_formatters import TodoFormatter, WorkspaceFormatter


class Formatter(ApiComponent):
    def __init__(self, app: App) -> None:
        self.todos = TodoFormatter(app)
        self.workspaces = WorkspaceFormatter(app)
        self.app = app
