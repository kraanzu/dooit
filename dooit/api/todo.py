from typing import List, Optional
from .model import Model


class Todo(Model):
    fields = ["about", "due", "urgency"]

    def __init__(self, parent: Optional["Model"] = None) -> None:
        super().__init__(parent)

        self.about = ""
        self.due = "today"
        self.urgency = 4
        self.status = "PENDING"
        self.todo_type = type(self)
        self.todos: List[Todo] = []

        self.opts = {
            "PENDING": "x",
            "COMPLETED": "X",
            "OVERDUE": "O",
        }

    def to_data(self) -> str:
        """
        Return todo.txt form of the todo
        """

        return f"{self.status} ({self.urgency}) due:{self.due or 'None'} {self.about}"

    def fill_from_data(self, data: str):
        """
        Setups obj from provided todo.txt form
        """

        status, urgency, due, *about = data.split()

        # status = self.opts[status]
        about = " ".join(about)

        due = due[4:]
        if due == "None":
            due = ""

        urgency = int(urgency[1:-1])

        self.about = about
        self.urgency = urgency
        self.due = due
        self.status = status

    def commit(self):
        """
        Returns obj data for storage
        """

        if self.todos:
            return [
                self.to_data(),
                [child.commit() for child in self.todos],
            ]
        else:
            return [
                self.to_data(),
            ]

    def add_child_todo(self):
        return super().add_child(Todo, self.todos)

    def add_sibling_todo(self):
        return super().add_sibling(Todo, self.todos)

    def shift_todo_up(self):
        return super().shift_up(self.todos)

    def shift_todo_down(self):
        return super().shift_down(self.todos)

    def next_todo(self):
        return super().next_sibling(self.todos)

    def prev_todo(self):
        return super().prev_sibling(self.todos)

    def remove_child_todo(self, name: str):
        return super().remove_child(self.todos, name)

    def drop_todo(self):
        return super().drop(self.todos)

    def sort_todo(self, attr: str):
        return super().sort_children(self.todos, attr)

    def from_data(self, data):
        """
        Setup obj from data
        """

        for i in data:
            self.add_child_todo()
            self.todos[-1].fill_from_data(i[0])
            if len(i) > 1:
                self.todos[-1].from_data(i[1])
