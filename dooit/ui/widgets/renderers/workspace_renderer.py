from rich.console import RenderableType
from rich.table import Table
from textual.app import events
from .base_renderer import BaseRenderer, Workspace
from dooit.ui.widgets.inputs.inputs import WorkspaceDescription
from dooit.ui.registry import registry


class WorkspaceRender(BaseRenderer):
    @property
    def model(self) -> Workspace:
        if not isinstance(self._model, Workspace):
            raise ValueError(f"Expected Workspace, got {type(self._model)}")
        return self._model

    def post_init(self):
        self.description = WorkspaceDescription(self.model)
        self.refresh_prompt()

    def _draw_description(self) -> RenderableType:

        description = self.description.render()
        return str(description)

    def _draw_table(self) -> Table:

        assert self.model.parent is not None

        table = registry.get_workspace_table(self.model.parent)
        layout = registry.get_workspace_layout()

        row = []
        for column, formatter in layout:
            row.append(getattr(self, f"_draw_{column.value}")())

        table.add_row(*row)

        return table

    def make_renderable(self) -> RenderableType:
        return self._draw_table()

    # TODO: Change this
    def handle_key(self, event: events.Key) -> bool:
        self.description.keypress(event.key)
        return True
