from typing import Generic, Iterable, Optional, TypeVar
from textual.app import events
from textual.widgets.option_list import Option
from collections import defaultdict
from dooit.api.model import DooitModel
from dooit.ui.events.events import ModeChanged
from dooit.ui.widgets.renderers.base_renderer import BaseRenderer
from .base_tree import BaseTree
from ._render_dict import RenderDict

ModelType = TypeVar("ModelType", bound=DooitModel)
RenderDictType = TypeVar("RenderDictType", bound=RenderDict)


class ModelTree(BaseTree, Generic[ModelType, RenderDictType]):
    DEFAULT_CSS = """
    ModelTree {
        height: 1fr;
        width: 1fr;
    }
    """

    def __init__(self, model: ModelType, render_dict: RenderDictType) -> None:
        tree = self.__class__.__name__
        super().__init__(id=f"{tree}_{model.uuid}")
        self._model = model
        self.expaned = defaultdict(bool)
        self._renderers: RenderDictType = render_dict

    def create_render(self, _: ModelType) -> RenderDictType:
        raise NotImplementedError

    @property
    def current(self) -> BaseRenderer:
        _id = self.node.id
        assert _id is not None

        return self._renderers[_id]

    def update_current_prompt(self):
        self.node.set_prompt(self.current.prompt)

    @property
    def is_editing(self) -> bool:
        return self.highlighted is not None and self.current.editing != ""

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
        res = self.current.start_edit(property)
        self.refresh_options()
        if res:
            self.app.post_message(ModeChanged("INSERT"))
            self.update_current_prompt()
            self.refresh_options()
        return res

    def stop_edit(self):
        self.current.stop_edit()
        self.app.post_message(ModeChanged("NORMAL"))

    def create_node(self):
        raise NotImplementedError

    async def handle_key(self, event: events.Key) -> bool:
        key = event.key
        if self.is_editing:
            if key == "escape":
                self.stop_edit()
            else:
                self.current.handle_key(event)

            self.update_current_prompt()
            self.refresh_options()
            return True
        else:
            return await super().handle_key(event)

    def refresh_options(self) -> None:
        for i in self._options:
            assert i.id is not None

            i.set_prompt(self._renderers[i.id].prompt)

        self._refresh_lines()

    def _get_parent(self, id: str) -> Optional[ModelType]:
        raise NotImplementedError

    def _get_children(self, id: str) -> Iterable[ModelType]:
        raise NotImplementedError

    def _insert_nodes(self, index: int, items: Iterable[Option]) -> None:
        if not items:
            return

        highlighted = self.highlighted
        opts = self._options
        opts = opts[:index] + list(items) + opts[index:]

        self.clear_options()
        self.add_options(opts)
        self.highlighted = highlighted

    def add_nodes(self, *items: Option, index: Optional[int] = None) -> None:
        if index is None:
            index = self.option_count

        self._insert_nodes(index, items)

    def _expand_node(self, _id: str) -> None:
        self.expanded_nodes[_id] = True
        options = self._get_children(_id)
        formatted_options = []

        for option in options:
            render = self._renderers[option.uuid]
            formatted_options.append(Option(render.prompt, id=render.id))

        index = self.get_option_index(_id)
        self._insert_nodes(index + 1, formatted_options)

    def expand_node(self) -> None:
        if self.highlighted is not None and self.node.id:
            self._expand_node(self.node.id)

    def _collapse_node(self, _id: str) -> None:
        self.expanded_nodes[_id] = False
        children = self._get_children(_id)
        for child in children:
            if child_id := child.uuid:
                self.remove_option(child_id)

    def collapse_node(self) -> None:
        if self.node.id:
            self._collapse_node(self.node.id)

    def _toggle_expand_node(self, _id: str) -> None:
        expanded = self.expanded_nodes[_id]
        if expanded:
            self._collapse_node(_id)
        else:
            self._expand_node(_id)

    def toggle_expand(self) -> None:
        if self.highlighted is None or not self.node.id:
            return

        self._toggle_expand_node(self.node.id)

    def _toggle_expand_parent(self, _id: str) -> None:
        parent = self._get_parent(_id)

        if not parent:
            return

        parent_id = parent.uuid
        self.highlighted = self.get_option_index(parent_id)
        self._toggle_expand_node(parent_id)

    def toggle_expand_parent(self) -> None:
        if self.highlighted is None:
            return

        if not self.node.id:
            return

        self._toggle_expand_parent(self.node.id)
