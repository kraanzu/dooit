from collections import defaultdict
from typing import Callable, List, Optional

from ._base import ApiComponent
from dooit.ui.events.events import ModeType

KeyBindType = defaultdict[str, defaultdict[str, Optional[Callable]]]


class KeyManager(ApiComponent):
    def __init__(self, get_mode: Callable) -> None:
        self.keybinds: KeyBindType = defaultdict(lambda: defaultdict(lambda: None))
        self._inputs: List[str] = []
        self.get_mode = get_mode

    def __set_key(self, mode: ModeType, key: str, callback: Callable) -> None:
        self.keybinds[mode][key] = callback

    def set_normal(self, key: str, callback: Callable) -> None:
        self.__set_key("NORMAL", key, callback)

    @property
    def input(self) -> str:
        return ",".join([i.strip() for i in self._inputs])

    def clear_input(self):
        self._inputs.clear()

    def search_for_key(self) -> Optional[Callable]:
        mode = self.get_mode()
        func = self.keybinds[mode].get(self.input)
        self.clear_input()

        return func

    def register_key(self, key: str) -> Optional[Callable]:
        self._inputs.append(key)
        return self.search_for_key()
