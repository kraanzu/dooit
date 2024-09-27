from typing import Callable, Optional
from uuid import uuid4
from dataclasses import dataclass


@dataclass
class FormatterFunc:
    name: str
    func: Callable


class FormatterStore:
    def __init__(self) -> None:
        self.formatters = dict()

    def add(self, func: Callable, id: Optional[str] = None) -> str:
        id = id or uuid4().hex
        self.formatters[id] = FormatterFunc(id, func)
        return id

    def remove(self, id: str) -> None:
        self.formatters.pop(id, None)
