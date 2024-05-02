from typing import Iterable, Optional

from dooit.api.todo import Todo
from .model_tree import ModelTree
from ..renderers.todo_renderer import TodoRender


class TodosTree(ModelTree):
    @property
    def node(self) -> TodoRender:
        option = super().node
        if not isinstance(option, TodoRender):
            raise ValueError(f"Expected WorkspaceRender, got {type(option)}")

        return option

    def get_option(self, option_id: str) -> TodoRender:
        option = super().get_option(option_id)
        if not isinstance(option, TodoRender):
            raise ValueError(f"Expected TodoRender, got {type(option)}")

        return option

    def _get_parent(self, id: str) -> Optional[TodoRender]:
        todo_model = self.get_option(id).model
        if isinstance(todo_model.parent, Todo):
            return TodoRender(todo_model.parent)

    def _get_children(self, id: str) -> Iterable[TodoRender]:
        todo_model = self.get_option(id).model
        return [TodoRender(todo) for todo in todo_model.todos]

    def force_refresh(self) -> None:
        self.clear_options()

        for todo in self.model.todos:
            self.add_option(TodoRender(todo))

    def _switch_to_workspace(self) -> None:
        if not self.node.id:
            return

        self.screen.query_one(f"WorkspacesTree").focus()

    def add_todo(self) -> str:
        workspace = self.model.add_child("todo")
        self.add_option(TodoRender(workspace))
        return workspace.uuid

    def create_node(self):
        uuid = self.add_todo()
        self.highlighted = self.get_option_index(uuid)
        self.start_edit("description")
