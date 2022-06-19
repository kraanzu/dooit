from pathlib import Path
from os import mkdir
from pickle import dump, load, HIGHEST_PROTOCOL
from dooit.ui.widgets.entry import Entry
from dooit.ui.widgets.navbar import Navbar
from dooit.ui.widgets.simple_input import SimpleInput
from dooit.ui.widgets.todo_list import TodoList


class Parser:
    def __init__(self) -> None:
        self.check_files()

    async def parse_todo(self) -> dict[str, TodoList]:
        return await self.load_todo()

    async def parse_topic(self) -> Navbar:
        return await self.load_topic()

    # --------------------------------

    async def load_topic(self) -> Navbar:
        with open(self.topic_path, "rb") as f:
            return await self.convert_topic(load(f))

    async def load_todo(self) -> dict[str, TodoList]:
        with open(self.todo_path, "rb") as f:
            return {i: await self.convert_todo(j) for i, j in load(f).items()}

    # --------------------------------

    async def convert_todo(self, e) -> TodoList:
        x = TodoList()
        for i, j in e:
            s = Entry.from_encoded(i)
            await x.root.add("", s)
            for k in j:
                s = Entry.from_encoded(k)
                await x.root.children[-1].add("", s)

        return x

    async def convert_topic(self, e) -> Navbar:
        x = Navbar()
        for i, j in e:
            s = SimpleInput()
            s.value = i
            await x.root.add("", s)
            for k in j:
                s = SimpleInput()
                s.value = k
                await x.root.children[-1].add("", s)

        return x

    # --------------------------------

    def fetch_usable_info_todo(self, todo: TodoList) -> list:
        x = []
        for i in todo.root.children:
            x.append([i.data.encode(), [j.data.encode() for j in i.children]])

        return x

    def fetch_usable_info_topic(self, topic: Navbar) -> list:
        x = []
        for i in topic.root.children:
            x.append([i.data.value, [j.data.value for j in i.children]])

        return x

    # --------------------------------

    def save_todo(self, todo: dict[str, TodoList]) -> None:
        with open(self.todo_path, "wb") as f:
            x = {i: self.fetch_usable_info_todo(j) for i, j in todo.items()}
            dump(x, f)

    def save_topic(self, topic) -> None:
        with open(self.topic_path, "wb") as f:
            dump(self.fetch_usable_info_topic(topic), f)

    # --------------------------------

    def check_files(self) -> None:
        config = Path.home() / ".config"
        if not Path.is_dir(config):
            mkdir(config)

        dooit = config / "dooit"
        if not Path.is_dir(dooit):
            mkdir(dooit)

        self.todo_path = dooit / "todos.pkl"
        if not Path.is_file(self.todo_path):
            with open(self.todo_path, "wb") as f:
                dump(
                    {"/": []},
                    f,
                    protocol=HIGHEST_PROTOCOL,
                )

        self.topic_path = dooit / "topics.pkl"
        if not Path.is_file(self.topic_path):
            with open(self.topic_path, "wb") as f:
                dump(
                    [],
                    f,
                    protocol=HIGHEST_PROTOCOL,
                )
