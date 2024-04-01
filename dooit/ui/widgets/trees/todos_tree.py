from typing import Iterable
from .model_tree import ModelTree
from ..renderers.todo_renderer import TodoRender


class TodosTree(ModelTree):
    def get_option(self, option_id: str) -> TodoRender:
        option = super().get_option(option_id)
        if not isinstance(option, TodoRender):
            raise ValueError(f"Expected TodoRender, got {type(option)}")

        return option

    def _get_children(self, id: str) -> Iterable[TodoRender]:
        todo_model = self.get_option(id).model
        return [TodoRender(todo) for todo in todo_model.todos]

    def force_refresh(self) -> None:
        self.clear_options()

        for todo in self.model.todos:
            self.add_option(TodoRender(todo))
