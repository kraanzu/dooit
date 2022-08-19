from typing import Optional

from dooit.utils import Todo, Urgency


class Topic:
    """
    Topic manager
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.todos: dict[str, Todo] = dict()

    def rename(self, name) -> None:
        self.name = name

    def add_todo(
        self,
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Urgency = Urgency.D,
    ):
        todo = Todo(about, due, urgency)
        self.todos[todo.id] = todo
