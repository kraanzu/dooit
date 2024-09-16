from typing import Optional


class InputCache:
    def __init__(self):
        self.cache = dict()

    def get(self, id: str, attr: str, value: str) -> Optional[int]:
        key = (id, attr, value)
        return self.cache.get(key)

    def set(self, id: str, attr: str, value: str, cached_value: int) -> None:
        key = (id, attr, value)
        self.cache[key] = cached_value


input_cache = InputCache()
