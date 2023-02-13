from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional, Union
from dooit.utils.conf_reader import Config

configured_keys = Config().get("keybindings")


class Bind:
    exclude_cursor_check = [
        "add_sibling",
        "change_status",
        "move_down",
        "move_up",
        "switch_pane",
        "spawn_help",
        "start_search",
        "stop_search",
    ]

    def __init__(self, func_name: str, params: List[str]) -> None:
        self.func_name = func_name
        self.params = params
        self.check_for_cursor = func_name not in self.exclude_cursor_check


KeyList = Dict[str, Union[str, List]]
PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
DEFAULTS = {
    "stop search": "<escape>",
    "switch pane": "<tab>",
    "move up": ["k", "<up>"],
    "shift up": ["K", "<shift+up>"],
    "move down": ["j", "<down>"],
    "shift down": ["J", "<shift+down>"],
    "edit description": "i",
    "toggle expand": "z",
    "toggle expand parent": "Z",
    "add child": "A",
    "add sibling": "a",
    "remove item": "x",
    "move to top": ["g", "<home>"],
    "move to bottom": ["G", "<end>"],
    "sort menu toggle": "s",
    "start search": "/",
    "spawn help": "?",
    "copy text": "y",
    "toggle complete": "c",
    "edit due": "d",
    "edit tags": "t",
    "edit recurrence": "r",
    "increase urgency": ["+", "="],
    "decrease urgency": ["-", "_"],
}

configured_keys = DEFAULTS | configured_keys


class KeyBinder:
    # KEYBIND MANAGER FOR NORMAL MODE

    def __init__(self) -> None:
        self.pressed = ""
        self.methods: Dict[str, Bind] = {}
        self.raw: DefaultDict[str, List[str]] = defaultdict(list)
        self.add_keys(configured_keys)

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
                if k not in self.raw[cmd]:
                    self.raw[cmd].append(k)

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
            if len(possible_keys) == 1 and possible_keys[0] == self.pressed:
                method = self.methods.get(possible_keys[0])
                self.clear()
                return method
            else:
                return Bind("change_status", ["K PENDING"])
        else:
            self.clear()
            return Bind("change_status", ["NORMAL"])
