from dataclasses import dataclass
from typing import Dict, List, Optional, Union


@dataclass
class Bind:
    func: str
    params: List[str]


KeyList = Dict[str, Union[str, List]]
PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
DEFAULTS = {
    "stop search": "<escape>",
    "switch tabs": "<tab>",
    "move up": ["k", "<up>"],
    "shift up": ["K", "<shift+up>"],
    "move down": ["j", "<down>"],
    "shift down": ["J", "<shift+down>"],
    "edit desc": "i",
    "toggle expand": "z",
    "toggle expand parent": "Z",
    "add child": "A",
    "add sibling": "a",
    "remove item": "x",
    "move to top": ["g", "<home>"],
    "move to bottom": ["<end>", "G"],
    "sort menu toggle": "s",
    "start search": "/",
    "spawn help": "?",
    "copy text": "y",
}

TODO_BINDINGS = {
    "toggle complete": "c",
    "edit due": "d",
    "edit tags": "t",
    "edit recur": "r",
    "edit eta": "e",
    "increase urgency": ["+", "="],
    "decrease urgency": ["-", "_"],
}


class KeyBinder:
    # KEYBIND MANAGER FOR NORMAL MODE

    def __init__(self, attach_todo_bindings: bool = False) -> None:
        self.pressed = ""
        self.methods: Dict[str, Bind] = {}
        self.add_keys(DEFAULTS)
        if attach_todo_bindings:
            self.add_keys(TODO_BINDINGS)

    def convert_to_bind(self, cmd: str):
        func_split = cmd.split()
        if func_split[0] == "edit":
            return Bind("start_edit", [func_split[1]])
        else:
            return Bind("_".join(func_split), [])

    def add_keys(self, keys: KeyList) -> None:
        for cmd, key in keys.items():
            if isinstance(key, str):
                key = [key]

            for k in key:
                self.methods[k] = self.convert_to_bind(cmd)

    def attach_key(self, key: str) -> None:
        if key == "escape" and self.pressed:
            return self.clear()

        if len(key) > 1:
            key = f"<{key}>"

        self.pressed += key

    def clear(self) -> None:
        self.pressed = ""

    def find_keys(self) -> List:

        possible_bindings = filter(
            lambda keybind: keybind.startswith(self.pressed),
            self.methods.keys(),
        )
        return list(possible_bindings)

    def get_method(self) -> Optional[Bind]:

        possible_keys = self.find_keys()
        if self.pressed and possible_keys:
            if len(possible_keys) == 1:
                method = self.methods.get(possible_keys[0])
                self.clear()
                return method
            else:
                return Bind("change_status", ["K PENDING"])
        else:
            self.clear()
            return Bind("change_status", ["NORMAL"])
