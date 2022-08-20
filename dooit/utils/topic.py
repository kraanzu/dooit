from typing import Optional

from dooit.utils.todo import Todo
from dooit.utils.urgency import Urgency


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
        urgency: Optional[Urgency] = None,
    ):
        todo = Todo(about, due, urgency)
        self.todos[todo.id] = todo

    def edit_todo(
        self,
        id_: str,
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Optional[Urgency] = None,
    ):
        self.todos[id_].edit(about, due, urgency)
