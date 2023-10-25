from typing import Optional
from textual.widget import Widget
from dooit.ui.events.events import ChangeStatus, Notify, StatusType
from dooit.utils.keybinder import KeyBinder, KeyList
from dooit.api.model import Result


class KeyWidget(Widget):
    """
    A widget that calls function from keybinder
    """

    def __init__(
        self,
        *children: Widget,
        name: Optional[str] = None,
        id: Optional[str] = None,
        classes: Optional[str] = None,
        disabled: bool = False
    ) -> None:
        super().__init__(
            *children, name=name, id=id, classes=classes, disabled=disabled
        )
        self.key_manager = KeyBinder()

    @property
    def is_cursor_available(self) -> bool:
        return True

    def add_keys(self, keys: KeyList):
        self.key_manager.add_keys(keys)

    async def keypress(self, key: str):
        self.key_manager.attach_key(key)
        bind = self.key_manager.get_method()
        if bind:
            if hasattr(self, bind.func_name):
                func = getattr(self, bind.func_name)
                if bind.check_for_cursor and not self.is_cursor_available:
                    return

                res = await func(*bind.params)
                if isinstance(res, Result) and res.message:
                    self.post_message(Notify(res.text()))

        self.refresh()


class HelperWidget(KeyWidget):
    """
    Helper Widgets to Tree Widgets
    Currently base for `SortOptions` and `SearchMenu`
    """

    DEFAULT_CSS = """
    HelperWidget {
        layer: L1;
        display: none;
    }
    """

    _status: StatusType

    async def hide(self) -> None:
        self.styles.layer = "L1"
        self.display = False
        self.post_message(ChangeStatus("NORMAL"))

    async def start(self) -> None:
        self.styles.layer = "L4"
        self.display = True
        self.post_message(ChangeStatus(self._status))

    async def cancel(self) -> None:
        await self.hide()

    async def stop(self):
        pass
