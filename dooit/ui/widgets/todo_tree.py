from typing import Optional
from dooit.ui.widgets.formatters.todo_tree_formatter import TodoFormatter

from dooit.utils.conf_reader import Config
from dooit.utils.keybinder import KeyBinder

from .tree import TreeList
from ...api.todo import Todo
from ...ui.events.events import SwitchTab
from ...api import Workspace

conf = Config()
EMPTY_TODO = conf.get("EMPTY_TODO")
dashboard = conf.get("dashboard")
PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
COLUMN_ORDER = conf.get("COLUMN_ORDER")
format = conf.get("TODO")


class TodoTree(TreeList):
    """
    Tree structured Class to manage todos
    """

    options = Todo.fields
    EMPTY = dashboard
    model_kind = "todo"
    model_type = Todo
    styler = TodoFormatter(format)
    COLS = COLUMN_ORDER
    key_manager = KeyBinder(attach_todo_bindings=True)

    def _get_children(self, model: Workspace):
        if model:
            return model.todos
        return []

    async def switch_tabs(self):
        if self.filter.value:
            await self.stop_search()

        await self.emit(SwitchTab(self))

    async def update_table(self, model: Optional[Workspace] = None):
        if not model:
            self.EMPTY = dashboard
            self.model = None
            self._refresh_rows()
        else:
            self.EMPTY = EMPTY_TODO
            if not self.item or not self.component:
                self.model = model
                self.current = -1
                self._refresh_rows()
            else:
                editing = self.editing
                path = self.item.path
                _old_val = ""

                if editing != "none":
                    _old_val = self.component.fields[editing].value
                    await self._cancel_edit()

                self.model = model
                self._refresh_rows()

                self.current = -1
                for i, j in enumerate(self.row_vals):
                    if j.item.path == path:
                        self.current = i
                        if editing != "none":
                            self.component.fields[editing].value = _old_val
                            await self.component.fields[editing].handle_keypress("end")
                            await self.start_edit(editing)
                        break

        self.refresh()

    def _setup_table(self) -> None:
        super()._setup_table(format["pointer"])
        for col in COLUMN_ORDER:
            if col == "desc":
                d = {"ratio": 1}
            elif col == "due":
                d = {"width": 20}
            elif col == "urgency":
                d = {"width": 1}
            else:
                raise TypeError

            self.table.add_column(col, **d)

    # ##########################################

    async def increase_urgency(self):
        if self.component and self.item:
            self.component.refresh()
            self.item.increase_urgency()

    async def decrease_urgency(self):
        if self.component and self.item:
            self.component.refresh()
            self.item.decrease_urgency()

    async def toggle_complete(self):
        if self.item and self.component:
            self.component.refresh()
            self.item.toggle_complete()

    # async def check_extra_keys(self, event: events.Key):
    #
    #     key = (
    #         event.character
    #         if (event.character and (event.character in PRINTABLE))
    #         else event.key
    #     )
    #
    #     if self.editing != "none":
    #         return
    #     if key in "d":
    #         await self.start_edit("due")
    #     elif key in "e":
    #         await self.start_edit("eta")
    #     elif key in "t":
    #         await self.start_edit("tags")
    #     elif key in "r":
    #         await self.start_edit("recur")
    #     elif key in "c":
    #         await self.toggle_complete()
    #     elif key in "+=":
    #         await self.increase_urgency()
    #     elif key in "_-":
    #         await self.decrease_urgency()
