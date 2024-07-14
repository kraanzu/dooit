from typing import List, Optional

from textual import on
from dooit.api.workspace import Workspace
from dooit.ui.widgets.switcher import FlexibleSwitcher
from dooit.ui.widgets.trees.todos_tree import TodosTree
from .model_tree import ModelTree
from ..renderers.workspace_renderer import WorkspaceRender


class WorkspacesTree(ModelTree):
    @property
    def is_editing(self) -> bool:
        return self.highlighted is not None and self.node.editing != ""

    @property
    def node(self) -> WorkspaceRender:
        option = super().node
        if not isinstance(option, WorkspaceRender):
            raise ValueError(f"Expected WorkspaceRender, got {type(option)}")

        return option

    def get_option(self, option_id: str) -> WorkspaceRender:
        option = super().get_option(option_id)
        if not isinstance(option, WorkspaceRender):
            raise ValueError(f"Expected WorkspaceRender, got {type(option)}")

        return option

    def _get_parent(self, id: str) -> Optional[WorkspaceRender]:
        todo_model = self.get_option(id).model
        if isinstance(todo_model.parent, Workspace):
            return WorkspaceRender(todo_model.parent)

    def _get_children(self, id: str) -> List[WorkspaceRender]:
        workspace_model = self.get_option(id).model
        return [WorkspaceRender(workspace) for workspace in workspace_model.workspaces]

    def force_refresh(self) -> None:
        self.clear_options()

        for workspace in self.model.workspaces:
            self.add_option(WorkspaceRender(workspace))

    @on(ModelTree.OptionHighlighted)
    def update_todo_tree(self, event: ModelTree.OptionHighlighted):
        if not event.option_id:
            return

        switcher = self.screen.query_one("#todo_switcher", expect_type=FlexibleSwitcher)
        todo_obj = self.get_option(event.option_id).model
        tree = TodosTree(todo_obj)

        if not self.screen.query(f"#{tree.id}"):
            switcher.add_widget(tree)

        switcher.current = tree.id

    def _switch_to_todos(self) -> None:
        try:
            if not self.node.id:
                return

            tree = TodosTree(self.node.model)
            self.screen.query_one(f"#{tree.id}", expect_type=TodosTree).focus()
        except ValueError:
            self.notify("No workspace selected")

    def add_workspace(self) -> str:
        workspace = self.model.add_child("workspace")
        self.add_option(WorkspaceRender(workspace))
        return workspace.uuid

    def create_node(self):
        uuid = self.add_workspace()
        self.highlighted = self.get_option_index(uuid)
        self.start_edit("description")
