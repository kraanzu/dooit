from typing import Iterable, Optional, Union

from textual.widgets.option_list import Option
from dooit.api import Todo, Workspace
from .model_tree import ModelTree
from ..renderers.todo_renderer import TodoRender
from ._render_dict import TodoRenderDict

Model = Union[Todo, Workspace]


class TodosTree(ModelTree[Model, TodoRenderDict]):

    def __init__(
        self,
        model: Model,
        render_dict: TodoRenderDict = TodoRenderDict(),
    ) -> None:
        super().__init__(model, render_dict)

    def _get_parent(self, id: str) -> Optional[Todo]:
        model = self._renderers[id].model
        return model

    def _get_children(self, id: str) -> Iterable[Todo]:
        model = self._renderers[id].model
        return model.todos

    def force_refresh(self) -> None:
        self.clear_options()

        for todo in self.model.todos:
            self.add_option(Option(self._renderers[todo.uuid].prompt, id=todo.uuid))

    def _switch_to_workspace(self) -> None:
        if not self.node.id:
            return

        self.screen.query_one("WorkspacesTree").focus()

    def add_todo(self) -> str:
        todo = self.model.add_todo()
        render = TodoRender(todo)
        self.add_option(Option(render.prompt, id=render.id))
        return todo.uuid

    def create_node(self):
        uuid = self.add_todo()
        self.highlighted = self.get_option_index(uuid)
        self.start_edit("description")
