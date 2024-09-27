from .._base import ApiComponent


class Formatter(ApiComponent):
    def __init__(self) -> None:
        self.todos = []
        self.workspaces = []
