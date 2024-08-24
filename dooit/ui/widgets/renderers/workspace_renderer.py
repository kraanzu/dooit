from rich.console import RenderableType
from rich.table import Table
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

    def post_init(self):
        self.description = WorkspaceDescription(self.model)

    def apply_formatters(self):
        layout = registry.get_workspace_layout()
        for item in layout:
            if isinstance(item, tuple):
                column, formatter = item
                component = self._get_component(column.value)
                component.add_formatter(formatter)

    def _draw_table(self) -> Table:

        assert self.model.parent is not None

        self.apply_formatters()
        table = registry.get_workspace_table(self.model.parent)
        layout = registry.get_workspace_layout()

        row = []
        for item in layout:
            if isinstance(item, tuple):
                item = item[0]

            row.append(self._get_component(item.value).render())

        table.add_row(*row)

        return table

    def make_renderable(self) -> RenderableType:
        return self._draw_table()

    # TODO: Change this
    def handle_key(self, event: events.Key) -> bool:
        self.description.keypress(event.key)
        return True
