from typing import Optional
from dooit.ui.formatters import TodoFormatter
from dooit.utils import KeyBinder, Config
from dooit.ui.events.events import SwitchTab
from dooit.api import Workspace, Todo
from .tree import TreeList

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

    options = Todo.sortable_fields
    EMPTY = dashboard
    model_kind = "todo"
    model_type = Todo
    styler = TodoFormatter(format)
    COLS = COLUMN_ORDER
    key_manager = KeyBinder()

    def _get_children(self, model: Workspace):
        if model:
            return model.todos
        return []

    async def switch_pane(self):
        if self.filter.value:
            await self.stop_search()

        await self.post_message(SwitchTab(self))

    async def update_table(self, model: Optional[Workspace] = None):
        self.EMPTY = EMPTY_TODO if model else dashboard
        self.model = model
        await self.rearrange()
        self.refresh()

    @property
    def item(self) -> Todo:
        return super().item

    def _setup_table(self) -> None:
        super()._setup_table(format["pointer"])
        for col in COLUMN_ORDER:
            if col == "description":
                d = {"ratio": 1}
            elif col == "due":
                # 12 -> size of formatted date
                # 02 -> padding
                d = {"width": 12 + 2 + len(format["due_icon"])}
            elif col == "urgency":
                d = {"width": 1}
            else:
                raise TypeError

            self.table.add_column(col, **d)

    # ##########################################

    async def increase_urgency(self):
        self.item.increase_urgency()
        self.commit()

    async def decrease_urgency(self):
        self.item.decrease_urgency()
        self.commit()

    async def toggle_complete(self):
        self.item.toggle_complete()
        self.commit()
