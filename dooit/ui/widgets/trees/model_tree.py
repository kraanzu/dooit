from dooit.api.model import Model
from collections import defaultdict

from dooit.ui.widgets.renderers.base_renderer import BaseRenderer
from .base_tree import BaseTree


class ModelTree(BaseTree):
    DEFAULT_CSS = """
    ModelTree {
        height: 100%;
        width: 100%;
    }
    """

    def __init__(self, model: Model) -> None:
        tree = self.__class__.__name__
        super().__init__(id=f"{tree}_{model.uuid}")
        self._model = model
        self.expaned = defaultdict(bool)

    @property
    def node(self) -> BaseRenderer:
        node = super().node
        if isinstance(node, BaseRenderer):
            return node

        raise ValueError(f"Expected BaseRenderer, got {type(node)}")

    @property
    def is_editing(self) -> bool:
        raise NotImplementedError

    @property
    def model(self) -> Model:
        return self._model

    def force_refresh(self) -> None:
        raise NotImplementedError

    def on_mount(self):
        self.force_refresh()

    def key_question_mark(self):
        self.app.push_screen("help")

    def start_edit(self, property: str) -> bool:
        res = self.node.start_edit(property)
        self.refresh_options()
        return res

    def stop_edit(self):
        self.node.stop_edit()
