from dooit.api.model import Model
from dooit.ui.widgets.todo import TodoWidget


class Clipboard:
    """
    Clipboard to copy models (Todos and Workspaces) as a whole
    """

    data = None

    def copy(self, widget: TodoWidget):
        model: Model = widget.model
        self.data = model.commit()

    @property
    def has_data(self) -> bool:
        return bool(self.data)
