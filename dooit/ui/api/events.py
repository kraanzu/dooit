from typing import Callable, Type
from dooit.ui.events.events import *  # noqa

DOOIT_EVENT_ATTR = "__dooit_event"


def subscribe(event: Type[DooitEvent]):
    """
    Subscribe decorator for event handlers
    """

    def decorator(func: Callable):
        setattr(func, DOOIT_EVENT_ATTR, event)
        return func

    return decorator
