from ._model_formatter_base import ModelFormatterBase
from .formatter_store import FormatterStore


class TodoFormatter(ModelFormatterBase):
    def setup_formatters(self):
        self.description = FormatterStore()
        self.due = FormatterStore()
        self.effort = FormatterStore()
        self.recurrence = FormatterStore()
        self.urgency = FormatterStore()
        self.status = FormatterStore()


class WorkspaceFormatter(ModelFormatterBase):
    def setup_formatters(self):
        self.description = FormatterStore()
