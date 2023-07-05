from typing import Optional
from dooit.ui.formatters import TodoFormatter
from dooit.utils import KeyBinder, Config
from dooit.ui.events.events import SwitchTab
from dooit.api import Workspace, Todo
from .tree import TreeList


class TodoTree(TreeList):
    """
    Tree structured Class to manage todos
    """

    def __init__(self):
        super().__init__()
        conf = Config()
        self.EMPTY_TODO = conf.get("EMPTY_TODO")
        self.dashboard = conf.get("dashboard")
        self.COLUMN_ORDER = conf.get("COLUMN_ORDER")
        self.format = conf.get("TODO")
        self.PRINTABLE = (
            "0123456789"
            + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
        )

        self.options = Todo.sortable_fields
        self.EMPTY = self.dashboard
        self.model_kind = "todo"
        self.model_type = Todo
        self.styler = TodoFormatter(self.format)
        self.COLS = self.COLUMN_ORDER
        self.key_manager = KeyBinder()
        
    def _get_children(self, model: Workspace):
        if model:
            if hasattr(model, 'todos'):
                return model.todos
        return []

    async def switch_pane(self):
        if self.filter.value:
            await self.stop_search()

        self.post_message(SwitchTab())

    async def update_table(self, model: Optional[Workspace] = None):
        self.EMPTY = self.EMPTY_TODO if model else self.dashboard
        self.model = model
        await self.rearrange()
        self.refresh()

    @property
    def item(self) -> Todo:
        return super().item

    def _setup_table(self) -> None:
        super()._setup_table(self.format["pointer"])
        for col in self.COLUMN_ORDER:
            if col == "description":
                d = {"ratio": 1}
            elif col == "due":
                # 12 -> size of formatted date
                # 02 -> padding
                d = {"width": 12 + 2 + len(self.format["due_icon"])}
            elif col == "urgency":
                d = {"width": 1}
            else:
                raise TypeError

            self.table.add_column(col, **d)

    # ##########################################

    async def increase_urgency(self):
        self.item.increase_urgency()
        self.commit()
        self._refresh_rows(True)

    async def decrease_urgency(self):
        self.item.decrease_urgency()
        self.commit()
        self._refresh_rows(True)

    async def toggle_complete(self):
        self.item.toggle_complete()
        self.commit()
        self._refresh_rows(True)
