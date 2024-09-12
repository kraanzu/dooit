from typing import Iterable, Optional, Union

from textual.widgets.option_list import Option
from dooit.api import Todo, Workspace
from .model_tree import ModelTree
from ..renderers.todo_renderer import TodoRender
from ._render_dict import TodoRenderDict

Model = Union[Todo, Workspace]


class TodosTree(ModelTree[Model, TodoRenderDict]):

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

    def add_todo(self) -> str:
        todo = self.model.add_todo()
        render = TodoRender(todo, tree=self)
        self.add_option(Option(render.prompt, id=render.id))
        return todo.uuid

    def create_node(self):
        uuid = self.add_todo()
        self.highlighted = self.get_option_index(uuid)
        self.start_edit("description")

    def _create_child_node(self) -> Todo:
        return self.current_model.add_todo()

    def force_refresh(self) -> None:
        highlighted = self.highlighted
        self.clear_options()

        options = []

        def add_children_recurse(model: Model):
            for child in model.todos:
                render = self._renderers[child.uuid]
                options.append(Option(render.prompt, id=render.id))

                if self.expanded_nodes[child.uuid]:
                    add_children_recurse(child)

        add_children_recurse(self.model)
        self.add_options(options)

        self.highlighted = highlighted
