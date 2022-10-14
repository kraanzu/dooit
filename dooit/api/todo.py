from typing import List, Optional, Type
from .model import Model

TODO = "todo"


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

        try:
            status, urgency, due, *about = data.split()
        except:
            raise TypeError(data)

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
        return super().add_child(TODO)

    def add_sibling_todo(self):
        return super().add_sibling(TODO)

    def shift_todo_up(self):
        return super().shift_up(TODO)

    def shift_todo_down(self):
        return super().shift_down(TODO)

    def next_todo(self):
        return super().next_sibling(TODO)

    def prev_todo(self):
        return super().prev_sibling(TODO)

    def remove_child_todo(self, name: str):
        return super().remove_child(TODO, name)

    def drop_todo(self):
        return super().drop(TODO)

    def sort_todo(self, attr: str):
        return super().sort_children(TODO, attr)

    def from_data(self, data: List):
        """
        Setup obj from data
        """

        # raise TypeError(f"{data}\n\n\n{data[1]}\n--------")
        self.fill_from_data(data[0])
        if len(data) > 1:
            for i in data[1]:
                child_todo: Todo = self.add_child_todo()
                child_todo.from_data(i)
