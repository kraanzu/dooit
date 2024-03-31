from typing import List
from .model_tree import ModelTree, Workspace
from ..renderers.workspace_renderer import WorkspaceRender


class WorkspacesTree(ModelTree):
    @property
    def model(self) -> Workspace:
        if not isinstance(self._model, Workspace):
            raise ValueError(f"Expected Workspace, got {type(self._model)}")

        return self._model

    def get_option(self, option_id: str) -> WorkspaceRender:
        option = super().get_option(option_id)
        if not isinstance(option, WorkspaceRender):
            raise ValueError(f"Expected WorkspaceRender, got {type(option)}")

        return option

    def _get_children(self, id: str) -> List[WorkspaceRender]:
        workspace_model = self.get_option(id).model
        return [WorkspaceRender(workspace) for workspace in workspace_model.workspaces]

    def force_refresh(self) -> None:
        self.clear_options()

        for workspace in self.model.workspaces:
            self.add_option(WorkspaceRender(workspace))
