from typing import Callable, Type
from dooit.ui.api.events import DooitEvent

DOOIT_EVENT_ATTR = "__dooit_event"
DOOIT_TIMER_ATTR = "__dooit_timer"


def subscribe(*events: Type[DooitEvent]):
    """
    Subscribe decorator for event handlers
    """

    def decorator(func: Callable):
        attrs = getattr(func, DOOIT_EVENT_ATTR, [])
        attrs.extend(events)

        setattr(func, DOOIT_EVENT_ATTR, attrs)
        return func

    return decorator


def timer(interval: float):
    """
    Timer decorator for event handlers
    """

    def decorator(func: Callable):
        setattr(func, DOOIT_TIMER_ATTR, interval)
        return func

    return decorator
