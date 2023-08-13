from textual.widget import Widget
from dooit.ui.events.events import Notify
from dooit.utils.keybinder import KeyBinder, KeyList
from dooit.api.model import Result


class KeyWidget(Widget):
    """
    A widget that calls function from keybinder
    """

    def __init__(
        self,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
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
