from .model_list import ModelTree, Todo
from ..renderers.todo_renderer import TodoRender


class TodosTree(ModelTree):
    @property
    def model(self) -> Todo:
        return self._model

    def force_refresh(self) -> None:
        self.clear_options()

        for todo in self.model.todos:
            self.add_option(TodoRender(todo))
