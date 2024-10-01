from typing import Callable


class EventDecorator:
    def __init__(self, event_name):
        self.event_name = event_name

    def __call__(self, func: Callable):
        setattr(func, "__dooit_event", self.event_name)
        return func


startup = EventDecorator("startup")
shutdown = EventDecorator("shutdown")
mode_changed = EventDecorator("mode_changed")
