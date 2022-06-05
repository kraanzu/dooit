from pathlib import Path
from os import mkdir
from dill import dump, load, HIGHEST_PROTOCOL
from doit.ui.widgets.navbar import Navbar
from doit.ui.widgets.todo_list import TodoList

DEFAULT = {'/': TodoList()}


class Parser:
    def parse_todo(self) -> dict[str, TodoList]:
        self.check_files()
        return self.load_todo()

    def parse_topic(self) -> Navbar:
        self.check_files()
        return self.load_topic()

    # --------------------------------

    def load_topic(self):
        with open(self.topic_path, "rb") as f:
            return load(f)

    def load_todo(self):
        with open(self.todo_path, "rb") as f:
            return load(f)

    # --------------------------------

    def save_todo(self, todo):
        with open(self.todo_path, "wb") as f:
            dump(todo, f)

    def save_topic(self, topic):
        with open(self.topic_path, "wb") as f:
            dump(topic, f)

    # --------------------------------

    def check_files(self) -> None:
        config = Path.home() / ".config"
        if not Path.is_dir(config):
            mkdir(config)

        doit = config / "doit"
        if not Path.is_dir(doit):
            mkdir(doit)

        self.todo_path = doit / "history"
        if not Path.is_file(self.todo_path):
            with open(self.todo_path, "wb") as f:
                dump(
                    DEFAULT,
                    f,
                    protocol=HIGHEST_PROTOCOL,
                )

        self.topic_path = doit / "topics"
        if not Path.is_file(self.topic_path):
            with open(self.topic_path, "wb") as f:
                dump(
                    Navbar(),
                    f,
                    protocol=HIGHEST_PROTOCOL,
                )

