from typing import List
from textual.app import events
from .base_renderer import BaseRenderer, Workspace
from dooit.ui.widgets.inputs.model_inputs import WorkspaceDescription
from dooit.ui.registry import registry


class WorkspaceRender(BaseRenderer):
    @property
    def model(self) -> Workspace:
        if not isinstance(self._model, Workspace):
            raise ValueError(f"Expected Workspace, got {type(self._model)}")
        return self._model

    @property
    def table_layout(self) -> List:
        return registry.get_workspace_layout()

    def post_init(self):
        self.description = WorkspaceDescription(self.model)

    def apply_formatters(self):
        layout = registry.get_workspace_layout()
        for item in layout:
            if isinstance(item, tuple):
                column, formatter = item
                component = self._get_component(column.value)
                component.add_formatter(formatter)

    # TODO: Change this
    def handle_key(self, event: events.Key) -> bool:
        self.description.keypress(event.key)
        return True
