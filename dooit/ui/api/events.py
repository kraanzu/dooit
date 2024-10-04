from typing import Callable, Type
from dooit.ui.events.events import *  # noqa


class Hook:
    def __init__(self, event: Type[DooitEvent]):
        self.event = event

    def __call__(self, func: Callable):
        setattr(func, "__dooit_event", self.event)
        return func


startup = Hook(Startup)
shutdown = Hook(ShutDown)
mode_changed = Hook(ModeChanged)
