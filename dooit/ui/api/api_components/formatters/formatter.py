from .._base import ApiComponent
from .model_formatters import TodoFormatter, WorkspaceFormatter


class Formatter(ApiComponent):
    def __init__(self) -> None:
        self.todos = TodoFormatter()
        self.workspaces = WorkspaceFormatter()
