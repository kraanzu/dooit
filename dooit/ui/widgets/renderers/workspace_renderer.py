from rich.console import RenderableType
from rich.table import Table
from textual.app import events
from .base_renderer import BaseRenderer, Workspace
from dooit.ui.widgets.inputs.inputs import WorkspaceDescription


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
        return self.description.render()

    def _draw_table(self) -> Table:
        table = Table.grid(expand=True)
        table.add_column("description", ratio=1)
        table.add_row(self._draw_description())
        return table

    def make_renderable(self) -> RenderableType:
        return self._draw_table()

    # TODO: Change this
    def handle_key(self, event: events.Key) -> bool:
        self.description.keypress(event.key)
        return True
