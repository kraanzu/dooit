from typing import Dict, List, Union
from rich.console import RenderableType
from rich.table import Table
from textual.app import events
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from dooit.ui.widgets.inputs.simple_input import SimpleInput

ModelType = Union[Todo, Workspace]


class BaseRenderer:
    editing: str = ""

    def __init__(self, model: ModelType, tree):
        self._model = model
        self.tree = tree
        self.post_init()

    def post_init(self):
        pass

    def _get_component(self, component: str) -> SimpleInput:
        return getattr(self, component)

    @property
    def id(self) -> str:
        return self._model.uuid

    @property
    def table_layout(self) -> List:
        raise NotImplementedError

    @property
    def prompt(self) -> RenderableType:
        return self.make_renderable()

    @property
    def model(self) -> ModelType:
        raise NotImplementedError

    def refresh_formatters(self):
        layout = self.table_layout
        for item in layout:
            if isinstance(item, tuple):
                column, formatter = item
                component = self._get_component(column.value)
                component.add_formatter(formatter)

    def _get_attr_width(self, attr: str) -> int:
        simple_input = self._get_component(attr)
        return max(
            len(simple_input.value),
            len(simple_input.render()),
        )

    def _get_max_width(self, attr: str) -> int:
        renderers: Dict = self.tree._renderers
        siblings = self.model.siblings

        return max(
            renderers[sibling.uuid]._get_attr_width(attr) for sibling in siblings
        )

    def make_renderable(self) -> RenderableType:
        self.refresh_formatters()

        layout = self.table_layout

        table = Table.grid(expand=True)
        row = []

        for item in layout:
            if isinstance(item, tuple):
                item = item[0]

            attr = item.value
            if attr == "description":
                table.add_column(attr, ratio=1)
            else:
                table.add_column(attr, width=self._get_max_width(attr))

            row.append(self._get_component(attr).render())

        table.add_row(*row)
        return table

    def start_edit(self, param: str) -> bool:
        if not hasattr(self, param):
            return False

        getattr(self, param).start_edit()
        self.editing = param
        return True

    def stop_edit(self):
        getattr(self, self.editing).stop_edit()
        self.editing = ""

    def handle_key(self, event: events.Key) -> bool:
        getattr(self, self.editing).keypress(event.character)
        return True
