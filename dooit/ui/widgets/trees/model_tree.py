from typing import Generic, TypeVar
from textual.app import events
from dooit.api.model import DooitModel
from collections import defaultdict
from dooit.ui.events.events import ModeChanged
from dooit.ui.widgets.renderers.base_renderer import BaseRenderer
from .base_tree import BaseTree

ModelType = TypeVar("ModelType", bound=DooitModel)


class ModelTree(BaseTree, Generic[ModelType]):
    DEFAULT_CSS = """
    ModelTree {
        height: 1fr;
        width: 1fr;
        background: magenta;
    }
    """

    def __init__(self, model: ModelType) -> None:
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
        return self.highlighted is not None and self.node.editing != ""

    @property
    def model(self) -> ModelType:
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
        if res:
            self.app.post_message(ModeChanged("INSERT"))
            self.node.refresh_prompt()
            self.refresh_options()
        return res

    def stop_edit(self):
        self.node.stop_edit()
        self.app.post_message(ModeChanged("NORMAL"))

    def create_node(self):
        raise NotImplementedError

    async def handle_key(self, event: events.Key) -> bool:
        key = event.key
        if self.is_editing:
            if key == "escape":
                self.stop_edit()
            else:
                self.node.handle_key(event)

            self.node.refresh_prompt()
            self.refresh_options()
            return True
        else:
            return await super().handle_key(event)
