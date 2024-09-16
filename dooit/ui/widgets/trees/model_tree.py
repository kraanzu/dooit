from typing import Generic, Iterable, Optional, TypeVar, Union
from textual.app import events
from textual.widgets.option_list import Option
from collections import defaultdict
from dooit.api import Todo, Workspace
from dooit.ui.events.events import ModeChanged
from dooit.ui.widgets.renderers.base_renderer import BaseRenderer
from .base_tree import BaseTree
from ._render_dict import RenderDict
from ._decorators import fix_highlight, refresh_tree

ModelType = TypeVar("ModelType", bound=Union[Todo, Workspace])
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

    @property
    def current(self) -> BaseRenderer:
        _id = self.node.id
        assert _id is not None

        return self._renderers[_id]

    @property
    def current_model(self) -> ModelType:
        return self.current.model

    def update_current_prompt(self):
        self.node.set_prompt(self.current.prompt)

    @property
    def is_editing(self) -> bool:
        return self.highlighted is not None and self.current.editing != ""

    @property
    def model(self) -> ModelType:
        return self._model

    @fix_highlight
    def force_refresh(self) -> None:
        self._force_refresh()

    def _force_refresh(self) -> None:
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

    @refresh_tree
    def _expand_node(self, _id: str) -> None:
        self.expanded_nodes[_id] = True

    def expand_node(self) -> None:
        if self.highlighted is not None and self.node.id:
            self._expand_node(self.node.id)

    @refresh_tree
    def _collapse_node(self, _id: str) -> None:
        self.expanded_nodes[_id] = False

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
        self.highlight_id(parent_id)
        self._toggle_expand_node(parent_id)

    def toggle_expand_parent(self) -> None:
        if self.highlighted is None:
            return

        if not self.node.id:
            return

        self._toggle_expand_parent(self.node.id)

    def _create_child_node(self) -> ModelType:
        raise NotImplementedError

    def add_child_node(self):

        node = self._create_child_node()
        node.description = "New Node"
        node.save()

        self.expand_node()
        self.highlight_id(node.uuid)
        self.start_edit("description")

    def _create_sibling_node(self) -> ModelType:
        return self.current_model.add_sibling()

    def highlight_id(self, _id: str):
        self.highlighted = self.get_option_index(_id)

    @refresh_tree
    def _add_sibling_node(self) -> ModelType:
        node = self._create_sibling_node()
        node.description = "New Node"
        node.save()
        return node

    def add_sibling(self):
        node = self._add_sibling_node()
        self.highlight_id(node.uuid)
        self.start_edit("description")

    @refresh_tree
    def remove_node(self):
        if self.highlighted is None:
            return

        self.current_model.drop()

    @refresh_tree
    def shift_up(self) -> None:
        self.current_model.shift_up()

    @refresh_tree
    def shift_down(self):
        self.current_model.shift_down()
