from typing import Dict, List, Union
from rich.console import RenderableType
from rich.table import Table
from textual.app import events

from dooit.api import Todo, Workspace
from ..inputs.simple_input import SimpleInput

ModelType = Union[Todo, Workspace]


class BaseRenderer:
    editing: str = ""

    def __init__(self, model: ModelType, tree):
        self._model = model
        self.tree = tree
        self.post_init()

    def post_init(self):
        pass

    def matches_filter(self, filter: str) -> bool:
        return filter in self.model.description

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
        return simple_input.get_max_width()

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

        # nested nodes as children
        if nest := self.model.nest_level:
            table.add_column("padding", width=2 * nest)
            row.append("")

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

    def handle_keypress(self, key: str) -> bool:
        getattr(self, self.editing).keypress(key)
        return True
