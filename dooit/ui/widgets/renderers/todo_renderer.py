from ..inputs.model_inputs import (
    Due,
    Effort,
    Recurrence,
    Status,
    TodoDescription,
    Urgency,
)
from .base_renderer import BaseRenderer, Todo


class TodoRender(BaseRenderer):
    @property
    def model(self) -> Todo:
        if not isinstance(self._model, Todo):
            raise ValueError(f"Expected Todo, got {type(self._model)}")
        return self._model

    def post_init(self):
        self.description = TodoDescription(self.model)
        self.due = Due(self.model)
        self.status = Status(self.model)
        self.urgency = Urgency(self.model)
        self.effort = Effort(self.model)
        self.recurrence = Recurrence(self.model)
