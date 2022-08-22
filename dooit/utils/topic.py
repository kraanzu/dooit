from typing import List, Optional

from dooit.utils.todo import Todo
from dooit.utils.urgency import Urgency


class Topic:
    """
    Topic manager
    """

    def __init__(self, name: str) -> None:
        self.name: str = name
        self.todos: List[Todo] = []

    def rename(self, name) -> None:
        self.name = name

    def _get_todo_index(self, id_):
        return [i for i, j in enumerate(self.todos) if j.id == id_][0]

    def todo(self, id_) -> Todo:
        idx = self._get_todo_index(id_)
        return self.todos[idx]

    def add_todo(
        self,
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Optional[Urgency] = None,
    ):
        todo = Todo(about, due, urgency)
        self.todos.append(todo)

    def edit_todo(
        self,
        id_: str,
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Optional[Urgency] = None,
    ):
        self.todo(id_).edit(about, due, urgency)
