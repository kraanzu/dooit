from typing import Any, List, Literal, Optional, Type, Union
from textual.app import ComposeResult
from textual.reactive import Reactive
from textual.widget import Widget
from dooit.api.workspace import Workspace
from dooit.api.model import Model, Ok, Result, Warn
from dooit.ui.events.events import (
    ChangeStatus,
    CommitData,
    DateModeSwitch,
    Notify,
    SpawnHelp,
    StatusType,
)
from dooit.ui.widgets.clipboard import Clipboard
from dooit.ui.widgets.empty import EmptyWidget
from dooit.ui.widgets.base import KeyWidget
from dooit.ui.widgets.search_menu import SearchMenu
from dooit.ui.widgets.sort_options import SortOptions
from dooit.ui.widgets.bar.status_bar import StatusBar
from dooit.ui.widgets.todo import TodoWidget
from dooit.ui.widgets.workspace import WorkspaceWidget

PRINTABLE = (
    "0123456789"
    + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
)


class Tree(KeyWidget, Widget):
    """
    Tree Widget to render items in tree format + funcs
    """

    ModelType = Workspace
    WidgetType = WorkspaceWidget
    current: Reactive[Optional[WidgetType]] = Reactive(None)
    clipboard = Clipboard()
    _rebuild_cache = True

    DEFAULT_CSS = """
    Tree {
        overflow: auto auto;
        scrollbar-size: 1 1;
    }
    """

    def __init__(self, model: Model, classes: str = ""):
        super().__init__(id=f"Tree-{model.uuid}", classes=classes)
        self.model = model

        tree_name = self.__class__.__name__
        self.border_title = tree_name.replace("Tree", "s")  # Making it plural
        self.sort_menu = SortOptions(self.ModelType)
        self.search_menu = SearchMenu(self.model, self.ModelType.class_kind)

    @property
    def is_cursor_available(self) -> bool:
        return bool(self.current) and self.current != -1

    @property
    def node(self) -> ModelType:
        if self.current:
            return self.current.model

        return self.model

    @property
    def visible_nodes(self) -> List[WidgetType]:
        if self._rebuild_cache:
            self._build()

        return self._visible_nodes_cache

    def _build(self):
        self._rebuild_cache = False
        self._visible_nodes_cache = [
            i for i in self.query(self.WidgetType) if i.is_visible
        ]

    @property
    def nodes(self) -> List[WidgetType]:
        return [
            widget
            for widget in self.walk_children()
            if isinstance(widget, self.WidgetType) and widget.display
        ]

    @property
    def model_class_kind(self) -> Literal["workspace", "todo"]:
        raise NotImplementedError

    @property
    def widget_type(self) -> Union[Type[WorkspaceWidget], Type[TodoWidget]]:
        raise NotImplementedError

    @property
    def current_visible_widget(self) -> Optional[Widget]:
        if self.sort_menu.styles.layer == "L4":
            return self.sort_menu

        if self.search_menu.styles.layer == "L4":
            return self.search_menu

    def get_children(self, parent: Model) -> List[ModelType]:
        return parent.workspaces

    def get_widget_by_id(self, id_: Any) -> WidgetType:
        return self.query_one(
            f"#{id_}",
            expect_type=self.WidgetType,
        )

    def change_highlights(
        self,
        old: Optional[WidgetType],
        new: Optional[WidgetType],
    ) -> None:
        with self.app.batch_update():
            if old:
                old.highlight(False)
            if new:
                try:
                    self.expand_parents(new)
                    new.highlight()
                except Exception:
                    self.post_message(Notify("can't find old highlighted node"))

    def expand_parents(self, widget: Optional[WidgetType]) -> None:
        """
        Expands all the ancestors in case of selection
        """

        if not widget:
            return

        with self.app.batch_update():
            parent = widget
            flag = False

            while parent and not parent.display:
                flag = True
                parent.display = True
                if not parent.expanded:
                    parent.toggle_expand()
                    self._rebuild_cache = True

                parent = parent.parent

            if flag and parent and not parent.expanded:
                parent.toggle_expand()
                self._rebuild_cache = True

    async def watch_current(
        self,
        old: Optional[WidgetType],
        new: Optional[WidgetType],
    ) -> None:
        self.change_highlights(old, new)

    def compose(self) -> ComposeResult:
        yield self.search_menu
        yield self.sort_menu
        children = self.get_children(self.model)

        if not children:
            yield EmptyWidget(self.model_class_kind)

        for i in children:
            yield self.WidgetType(i)

    async def force_refresh(self, model: Optional[Model] = None):
        """
        Refreshes the whole tree in case of change in storage file
        """

        highlighted = None
        if self.current:
            highlighted = self.current.id

        was_expanded = dict()
        for i in self.query(self.WidgetType):
            was_expanded[i.id] = getattr(i, "expanded", False)
            i.remove()

        if model:
            self.model = model

        children = self.get_children(self.model)

        if not children:
            self.current = None
            await self.mount(EmptyWidget(self.model_class_kind))
            return

        with self.app.batch_update():
            for i in children:
                widget = self.WidgetType(i)
                await self.mount(widget)

                if was_expanded.get(i.uuid, False):
                    widget.toggle_expand()

        self.current = None
        try:
            self.current = self.get_widget_by_id(highlighted)
        except Exception:
            pass
        self._rebuild_cache = True

    async def notify(self, message: str) -> None:
        self.post_message(Notify(message))

    def next_node(self) -> Optional[WidgetType]:
        nodes = self.visible_nodes
        if not nodes:
            return

        if not self.current:
            return nodes[0] if nodes else None

        idx = nodes.index(self.current)
        if idx == len(nodes) - 1:
            return

        return nodes[idx + 1]

    def prev_node(self) -> Optional[WidgetType]:
        nodes = self.visible_nodes

        if not nodes:
            return

        if not self.current:
            return

        idx = nodes.index(self.current)
        if not idx:
            return

        return nodes[idx - 1]

    async def shift_node(self, position: Literal["up", "down"]) -> None:
        if not self.current:
            return

        node = self.node
        expanded = self.current.expanded

        sibling = node.next_sibling() if position == "down" else node.prev_sibling()

        if sibling:
            sibling_id = sibling.uuid

            if position == "down":
                node.shift_down()
            else:
                node.shift_up()

            new_widget = self.WidgetType(node)
            if self.current:
                self.current.remove()

            sibling_widget = self.get_widget_by_id(sibling_id)
            if position == "down":
                await self.mount(new_widget, after=sibling_widget)
            else:
                await self.mount(new_widget, before=sibling_widget)

            self.current = new_widget
            if expanded:
                self.current.toggle_expand()

            new_widget.highlight()
            self.post_message(CommitData())
            self._rebuild_cache = True

    async def add_first_child(self) -> None:
        for i in self.query(EmptyWidget):
            self.styles.overflow_y = "auto"
            self.styles.overflow_x = "auto"
            await i.remove()

        child = self.model.add_child(self.ModelType.class_kind)
        new_widget = self.WidgetType(child)
        await self.mount(new_widget)
        self.current = new_widget
        await self.start_edit("description")

    async def add_node(
        self, type_: Literal["child", "sibling"], edit: bool = True
    ) -> None:
        if not self.get_children(self.model) or not self.current:
            return await self.add_first_child()

        if type_ == "child" and not self.current.expanded:
            self.current.toggle_expand()

        new_node = (
            self.node.add_child(self.ModelType.class_kind)
            if type_ == "child"
            else self.node.add_sibling()
        )

        widget = self.WidgetType(new_node)
        if type_ == "sibling":
            await self.mount(widget, after=self.current)
        else:
            await self.current.mount(widget)

        self.current = widget

        if edit:
            widget.start_edit("description")
        self._rebuild_cache = True

    async def remove_item(self) -> None:
        if not self.current:
            return

        widget = self.current

        if node := self.next_node():
            self.current = node
        elif node := self.prev_node():
            self.current = node
        else:
            self.current = None

            # NOTE: This hack is done because the app first renders
            # and then removes scrollbars which looks like a glitch

            self.styles.overflow_y = "hidden"
            self.styles.overflow_x = "hidden"
            await self.mount(EmptyWidget(self.model_class_kind))

        widget.model.drop()
        await widget.remove()
        self.post_message(CommitData())
        await self.change_status("NORMAL")
        self._rebuild_cache = True

    async def move_down(self) -> None:
        if node := self.next_node():
            self.current = node

    async def move_up(self) -> None:
        if node := self.prev_node():
            self.current = node

    async def move_to_top(self) -> None:
        if self.nodes:
            self.current = self.nodes[0]

    async def move_to_bottom(self) -> None:
        if self.nodes:
            self.current = self.nodes[-1]

    async def shift_down(self) -> None:
        return await self.shift_node("down")

    async def shift_up(self) -> None:
        return await self.shift_node("up")

    async def add_child(self) -> None:
        await self.add_node("child")

    async def add_sibling(self) -> None:
        await self.add_node("sibling")

    async def toggle_expand(self) -> None:
        if not self.current:
            return

        self.current.toggle_expand()
        self._rebuild_cache = True

    async def toggle_expand_parent(self) -> None:
        if not self.current:
            return

        id_ = self.current.toggle_expand_parent()
        if id_:
            self.current = self.get_widget_by_id(id_)
            if self.current.expanded:
                await self.toggle_expand()
        self._rebuild_cache = True

    async def copy_text(self) -> None:
        if not self.current:
            return

        await self.current.copy_text()
        self.post_message(Notify(Ok("Text was copied to clipboard!")))

    async def switch_pane(self) -> None:
        pass

    async def yank(self) -> None:
        if not self.current:
            return

        self.clipboard.copy(self.current)
        self.current.flash()
        self.post_message(
            Notify(Ok(f"{self.ModelType.__name__} was copied to clipboard!"))
        )

    async def paste(self) -> Result:
        if not self.current:
            return Warn()

        if not self.clipboard.has_data:
            return Warn("Nothing in the clipboard!")

        model = self.current.model.add_sibling()
        model.from_data(self.clipboard.data, False)
        widget = self.WidgetType(model)
        await self.mount(widget, after=self.current)
        self.current = widget
        return Ok()

    async def switch_pane_workspace(self) -> None:
        pass

    async def switch_pane_todo(self) -> None:
        pass

    async def start_edit(self, field: str) -> Result:
        if not self.current:
            return Warn("Nothing to edit!")

        return self.current.start_edit(field)

    async def stop_edit(self, res: Result) -> None:
        if not self.current:
            return

        self.post_message(CommitData())
        self.post_message(ChangeStatus("NORMAL"))
        self.current.refresh(layout=True)

        self.post_message(Notify(res.text()))
        if res.cancel_op:
            await self.remove_item()

    async def apply_filter(self, filter) -> None:
        for i in self.query(self.widget_type):
            await i.apply_filter(filter)

    async def apply_sort(self, id_: str, method: str) -> None:
        widget = self.get_widget_by_id(id_)
        widget.model.sort(method)
        await self.force_refresh()
        self.post_message(ChangeStatus("NORMAL"))

    async def sort_menu_toggle(self) -> None:
        if not self.current:
            self.post_message(Notify(Warn("No item selected!")))
            return

        self.sort_menu.set_id(str(self.current.id))
        if self.sort_menu.visible:
            await self.sort_menu.start()
        else:
            await self.sort_menu.stop()

    async def spawn_help(self) -> None:
        self.post_message(SpawnHelp())

    async def change_status(self, status: StatusType) -> None:
        self.post_message(ChangeStatus(status))

    async def start_search(self) -> None:
        if self.search_menu.id:
            self.search_menu.refresh_options()
            await self.search_menu.start()
            await self.app.query_one(StatusBar).start_search(self.search_menu.id)

    async def switch_date_style(self):
        self.post_message(DateModeSwitch())

    async def keypress(self, key: str) -> None:
        if self.current_visible_widget and hasattr(
            self.current_visible_widget, "keypress"
        ):
            return await getattr(self.current_visible_widget, "keypress")(key)

        if self.current and self.current._is_editing():
            return await self.current.keypress(key)

        await super().keypress(key)
