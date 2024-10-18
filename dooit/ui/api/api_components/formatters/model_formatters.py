from ._model_formatter_base import ModelFormatterBase
from dooit.ui.widgets.trees import TodosTree, WorkspacesTree


class TodoFormatter(ModelFormatterBase):
    def setup_formatters(self):
        self.description = self.get_formatter_store()
        self.due = self.get_formatter_store()
        self.effort = self.get_formatter_store()
        self.recurrence = self.get_formatter_store()
        self.urgency = self.get_formatter_store()
        self.status = self.get_formatter_store()

    def trigger(self) -> None:
        for widget in self.api.app.query(TodosTree):
            widget.force_refresh()


class WorkspaceFormatter(ModelFormatterBase):
    def setup_formatters(self):
        self.description = self.get_formatter_store()

    def trigger(self) -> None:
        for widget in self.api.app.query(WorkspacesTree):
            widget.force_refresh()
