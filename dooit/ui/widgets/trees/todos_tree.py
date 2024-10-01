from typing import TYPE_CHECKING, Iterable, Optional, Union
from textual.widgets.option_list import Option

from dooit.api import Todo, Workspace
from .model_tree import ModelTree
from ..renderers.todo_renderer import TodoRender
from ._render_dict import TodoRenderDict

if TYPE_CHECKING:  # pragma: no cover
    from ...api.api_components.formatters.model_formatters import (
        TodoFormatter,
    )

Model = Union[Todo, Workspace]


class TodosTree(ModelTree[Model, TodoRenderDict]):
    BORDER_TITLE = "Todos"

    def __init__(self, model: Model) -> None:
        super().__init__(model, TodoRenderDict(self))

    def _get_parent(self, id: str) -> Optional[Todo]:
        return Todo.from_id(id).parent_todo

    def _get_children(self, id: str) -> Iterable[Todo]:
        return Todo.from_id(id).todos

    def _switch_to_workspace(self) -> None:
        if not self.node.id:
            return

        self.screen.query_one("WorkspacesTree").focus()

    @property
    def formatter(self) -> "TodoFormatter":
        return self.api.formatter.todos

    @property
    def layout(self):
        return self.api.layouts.todo_layout

    def add_todo(self) -> str:
        todo = self.model.add_todo()
        render = TodoRender(todo, tree=self)
        self.add_option(Option(render.prompt, id=render.id))
        return todo.uuid

    def _add_first_item(self) -> Todo:
        return self.model.add_todo()

    def _create_child_node(self) -> Todo:
        return self.current_model.add_todo()
