from typing import List

from textual.widgets.option_list import Option
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

    def _get_children(self, id: str) -> List[Option]:
        obj = [i for i in self.model.workspaces if i.uuid == id][0]
        return [WorkspaceRender(workspace) for workspace in obj.workspaces]

    def force_refresh(self) -> None:
        self.clear_options()

        for workspace in self.model.workspaces:
            self.add_option(WorkspaceRender(workspace))
