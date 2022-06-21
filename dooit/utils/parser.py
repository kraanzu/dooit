import yaml
from pathlib import Path
from os import mkdir, remove
from pickle import dump, load, HIGHEST_PROTOCOL

from dooit.ui.widgets.entry import Entry
from dooit.ui.widgets.navbar import Navbar
from dooit.ui.widgets.simple_input import SimpleInput
from dooit.ui.widgets.todo_list import TodoList
from dooit.utils.config import DOOIT, HOME


class Parser:
    def __init__(self) -> None:
        self.check_files()

    def fix_deprecated(self):
        remove(self.old_topic_path)
        remove(self.old_todo_path)

    # --------------------------------

    def save(self, todo: dict[str, TodoList]):
        def make_yaml(todolist: TodoList):
            arr = {}
            for parent in todolist.root.children:
                txt = parent.data.to_txt()
                arr[txt] = []
                if children := parent.children:
                    arr[txt].extend([child.data.to_txt() for child in children])

            return arr

        todolist = {}
        for topic, task in todo.items():
            if not topic or topic == "/":
                continue

            if topic.count("/") == 1:
                todolist[topic[:-1]] = {"common": make_yaml(task)}
            else:
                idx = topic.index("/")
                super_topic = topic[:idx]
                sub = topic[idx + 1 : -1]
                todolist[super_topic][sub] = make_yaml(task)

        with open(self.todo_txt, "w") as f:
            yaml.safe_dump(todolist, f)

    async def load(self):
        if self.old_todo_path.is_file() and self.old_topic_path.is_file():
            x = (await self.load_topic(), await self.load_todo())
            self.fix_deprecated()
            return x

        with open(self.todo_txt, "r") as f:
            todos = yaml.safe_load(f) or dict()

        navbar = Navbar()
        todo_tree = {}

        for topic, subtopics in todos.items():
            s = SimpleInput()
            s.value = topic
            topic += "/"
            await navbar.root.add("", s)

            todo_tree[topic] = TodoList()

            for subtopic, parents in subtopics.items():
                for parent, childs in parents.items():
                    if subtopic == "common":
                        tree = todo_tree[topic]
                    else:
                        s = SimpleInput()
                        s.value = subtopic
                        await navbar.root.children[-1].add("", s)
                        name = topic + subtopic + "/"
                        todo_tree[name] = TodoList()
                        tree = todo_tree[name]

                    tree = tree.root
                    await tree.add("", Entry.from_txt(parent))

                    for child in childs:
                        await tree.children[-1].add("", Entry.from_txt(child))

        return navbar, todo_tree

    # --------------------------------

    # NOTE: Will be depracted in v0.3.0
    async def load_topic(self) -> Navbar:
        with open(self.old_topic_path, "rb") as f:
            return await self.convert_topic(load(f))

    # NOTE: Will be depracted in v0.3.0
    async def load_todo(self) -> dict[str, TodoList]:
        with open(self.old_todo_path, "rb") as f:
            return {i: await self.convert_todo(j) for i, j in load(f).items()}

    # --------------------------------

    # NOTE: Will be depracted in v0.3.0
    async def convert_todo(self, e) -> TodoList:
        x = TodoList()
        for i, j in e:
            s = Entry.from_encoded(i)
            await x.root.add("", s)
            for k in j:
                s = Entry.from_encoded(k)
                await x.root.children[-1].add("", s)

        return x

    # NOTE: Will be depracted in v0.3.0
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

    # NOTE: Will be depracted in v0.3.0
    def fetch_usable_info_todo(self, todo: TodoList) -> list:
        x = []
        for i in todo.root.children:
            x.append([i.data.encode(), [j.data.encode() for j in i.children]])

        return x

    # NOTE: Will be depracted in v0.3.0
    def fetch_usable_info_topic(self, topic: Navbar) -> list:
        x = []
        for i in topic.root.children:
            x.append([i.data.value, [j.data.value for j in i.children]])

        return x

    # --------------------------------

    def check_files(self) -> None:
        def check_folder(f):

            if not Path.is_dir(f):
                mkdir(f)

        config = Path.home() / ".config"
        check_folder(config)

        dooit = config / "dooit"
        check_folder(dooit)

        local = HOME / ".local"
        check_folder(local)

        share = local / "share"
        check_folder(share)

        dooit_data = share / "dooit"
        check_folder(dooit_data)

        self.old_todo_path = dooit / "todos.pkl"
        self.old_topic_path = dooit / "topics.pkl"

        self.todo_txt = dooit_data / "todo.yaml"
        if not Path.is_file(self.todo_txt):
            with open(self.todo_txt, "w") as f:
                yaml.safe_dump(
                    dict(),
                    f,
                )
