from typing import TYPE_CHECKING
from .._base import ApiComponent
from .model_formatters import TodoFormatter, WorkspaceFormatter

if TYPE_CHECKING:
    from dooit.ui.tui import Dooit


class Formatter(ApiComponent):
    def __init__(self, app: "Dooit") -> None:
        self.todos = TodoFormatter(app)
        self.workspaces = WorkspaceFormatter(app)
        self.app = app
