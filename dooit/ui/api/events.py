from typing import Callable, Type
from dooit.ui.events.events import *  # noqa


def subscribe(event: Type[DooitEvent]):
    """
    Subscribe decorator for event handlers
    """

    def decorator(func: Callable):
        setattr(func, "__dooit_event", event)
        return func

    return decorator
