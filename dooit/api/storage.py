from dataclasses import dataclass


@dataclass
class S_Storage:
    instance = None

    def __init__(self):
        S_Storage.instance = self
        self._clipboard = None


class Storage:
    clipboard = (
        S_Storage.instance._clipboard if S_Storage.instance else S_Storage()._clipboard
    )
