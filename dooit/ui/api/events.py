from typing import Callable, Type
from dooit.ui.events.events import *  # noqa


class Hooks:
    def __init__(self, event: Type[DooitEvent]):
        self.event = event

    def __call__(self, func: Callable):
        setattr(func, "__dooit_event", self.event)
        return func


startup = Hooks(Startup)
shutdown = Hooks(ExitApp)
mode_changed = Hooks(ModeChanged)
