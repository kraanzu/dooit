from ._model_formatter_base import ModelFormatterBase
from .formatter_store import FormatterStore
from dooit.ui.widgets.trees import TodosTree, WorkspacesTree


class TodoFormatter(ModelFormatterBase):
    def setup_formatters(self):
        self.description = FormatterStore(self.trigger)
        self.due = FormatterStore(self.trigger)
        self.effort = FormatterStore(self.trigger)
        self.recurrence = FormatterStore(self.trigger)
        self.urgency = FormatterStore(self.trigger)
        self.status = FormatterStore(self.trigger)

    def trigger(self) -> None:
        for widget in self.app.query(TodosTree):
            widget.force_refresh()


class WorkspaceFormatter(ModelFormatterBase):
    def setup_formatters(self):
        self.description = FormatterStore(self.trigger)

    def trigger(self) -> None:
        for widget in self.app.query(WorkspacesTree):
            widget.force_refresh()
