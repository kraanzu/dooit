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

    def set(self, keys: str, callback: Callable) -> None:
        for key in keys.split(","):
            self.__set_key("NORMAL", key, callback)

    @property
    def input(self) -> str:
        formatted = ""
        for i in self._inputs:
            if len(i) > 1 and len(self._inputs) > 1:
                formatted += f"<{i}>"
            else:
                formatted += i

        return formatted

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
