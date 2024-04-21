from dooit.api.model import Model
from collections import defaultdict
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

    # NOTE: remove thse methods later

    def key_j(self):
        self.action_cursor_down()

    def key_k(self):
        self.action_cursor_up()

    def key_z(self):
        self.toggle_expand()

    def key_upper_z(self):
        self.toggle_expand_parent()
