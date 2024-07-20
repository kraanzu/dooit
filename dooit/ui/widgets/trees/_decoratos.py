from typing import Callable
from dooit.api.model import Result


def node_required(func: Callable) -> Callable:
    def wrapper(self, *args, **kwargs) -> Result:
        if not self.has_items:
            return Result(False, True, "No items present")

        return func(self, *args, **kwargs)

    return wrapper
