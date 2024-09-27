from typing import Callable, Optional
from uuid import uuid4
from dataclasses import dataclass


@dataclass
class FormatterFunc:
    name: str
    func: Callable


def trigger_refresh(func: Callable) -> Callable:
    def wrapper(self: "FormatterStore", *args, **kwargs):
        res = func(self, *args, **kwargs)
        self.trigger()
        return res

    return wrapper


class FormatterStore:
    def __init__(self, trigger: Callable) -> None:
        self.formatters = dict()
        self.trigger = trigger

    @trigger_refresh
    def add(self, func: Callable, id: Optional[str] = None) -> str:
        id = id or uuid4().hex
        self.formatters[id] = FormatterFunc(id, func)
        return id

    @trigger_refresh
    def remove(self, id: str) -> None:
        self.formatters.pop(id, None)
