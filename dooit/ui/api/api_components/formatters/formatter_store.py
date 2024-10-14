from typing import Any, Callable, List, Optional
from uuid import uuid4
from dataclasses import dataclass

from dooit.api.workspace import ModelType


@dataclass
class FormatterFunc:
    name: str
    func: Callable
    disabled: bool = False
    previous_formatter: Optional["FormatterFunc"] = None


def trigger_refresh(func: Callable) -> Callable:
    def wrapper(self: "FormatterStore", *args, **kwargs):
        res = func(self, *args, **kwargs)
        self.trigger()
        return res

    return wrapper


class FormatterStore:
    def __init__(self, trigger: Callable, allow_multiple: bool = False) -> None:
        self.formatters = dict()
        self.trigger = trigger
        self.allow_multiple = allow_multiple

    @trigger_refresh
    def add(self, func: Callable, id: Optional[str] = None) -> str:
        id = id or uuid4().hex
        self.formatters[id] = FormatterFunc(
            id,
            func,
            previous_formatter=self.current_formatter,
        )
        return id

    @trigger_refresh
    def remove(self, id: str) -> None:
        self.formatters.pop(id, None)

    @trigger_refresh
    def disable(self, id: str) -> bool:
        formatter = self.formatters.get(id)
        if not formatter:
            return False
        formatter.disabled = True
        return True

    @trigger_refresh
    def enable(self, id: str, set_current: bool = False) -> bool:
        formatter = self.formatters.get(id)
        if not formatter:
            return False
        formatter.disabled = False

        if set_current:
            formatter = self.formatters.pop(id)
            self.formatters.update({id: formatter})

        return True

    @property
    def formatter_functions(self) -> List[Callable]:
        return [formatter.func for formatter in self.formatters.values()]

    @property
    def current_formatter(self) -> FormatterFunc:
        enabled_formatters = [i for i in self.formatters.values() if not i.disabled]
        if not enabled_formatters:
            return FormatterFunc("default", lambda x, _: str(x))

        return enabled_formatters[-1]

    def format_value(self, value: Any, model: ModelType) -> str:
        return self.current_formatter.func(value, model)
