from typing import List

from textual.widgets.option_list import Option
from .model_list import ModelList, Workspace
from ..renderers.workspace_renderer import WorkspaceRender


class WorkspacesList(ModelList):
    @property
    def model(self) -> Workspace:
        return self._model

    def _get_children(self, id: str) -> List[Option]:
        obj = [i for i in self.model.workspaces if i.uuid == id][0]
        return [WorkspaceRender(workspace) for workspace in obj.workspaces]

    def force_refresh(self) -> None:
        self.clear_options()

        for workspace in self.model.workspaces:
            self.add_option(WorkspaceRender(workspace))
