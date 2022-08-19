from dooit.utils import Todo


class Topic:
    """
    Topic manager
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.todos: list[Todo] = []

    def rename(self, name) -> None:
        self.name = name

