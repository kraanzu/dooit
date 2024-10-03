from typing import TYPE_CHECKING, List, Optional
from textual import on
from textual.widgets.option_list import Option

from dooit.api import Workspace
from dooit.ui.events.events import (
    WorkspaceDescriptionChanged,
    WorkspaceRemoved,
    WorkspaceSelected,
)
from .model_tree import ModelTree
from .todos_tree import TodosTree
from ._render_dict import WorkspaceRenderDict


if TYPE_CHECKING:  # pragma: no cover
    from dooit.ui.api.api_components.formatters.model_formatters import (
        WorkspaceFormatter,
    )


class WorkspacesTree(ModelTree[Workspace, WorkspaceRenderDict]):
    BORDER_TITLE = "Workspaces"

    def __init__(self, model: Workspace) -> None:
        render_dict = WorkspaceRenderDict(self)
        super().__init__(model, render_dict)

    def _get_parent(self, id: str) -> Optional[Workspace]:
        return Workspace.from_id(id).parent_workspace

    def _get_children(self, id: str) -> List[Workspace]:
        return Workspace.from_id(id).workspaces

    @property
    def formatter(self) -> "WorkspaceFormatter":
        return self.api.formatter.workspaces

    @property
    def layout(self):
        return self.api.layouts.workspace_layout

    def _switch_to_todos(self) -> None:
        try:
            if not self.node.id:
                return

            tree = TodosTree(self.current.model)
            self.screen.query_one(f"#{tree.id}", expect_type=TodosTree).focus()
        except ValueError:
            self.notify("No workspace selected")

    def add_workspace(self) -> str:
        workspace = self.model.add_workspace()
        renderer = self._renderers[workspace.uuid]
        self.add_option(Option(renderer.prompt, id=renderer.id))
        return workspace.uuid

    def _create_child_node(self) -> Workspace:
        return self.current_model.add_workspace()

    def _add_first_item(self) -> Workspace:
        return self.model.add_workspace()

    def _remove_node(self) -> None:
        self.post_message(WorkspaceRemoved(self.current_model))
        return super()._remove_node()

    @on(ModelTree.OptionHighlighted)
    def workspace_highlighted(self, event: ModelTree.OptionHighlighted):
        assert event.option_id

        event.stop()
        self.post_message(WorkspaceSelected(Workspace.from_id(event.option_id)))
