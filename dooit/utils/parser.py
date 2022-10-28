from typing import Dict
import yaml
from pathlib import Path
from os import mkdir, environ

HOME = Path.home()
XDG_CONFIG = HOME / ".config"


class Parser:
    def __init__(self) -> None:
        self.check_files()

    @classmethod
    def save(cls, data):
        obj = cls()
        with open(obj.todo_yaml, "w") as stream:
            yaml.safe_dump(data, stream)

    @classmethod
    def load(cls) -> Dict:
        obj = cls()
        with open(obj.todo_yaml, "r") as stream:
            data = yaml.safe_load(stream)

        return data

    def check_files(self) -> None:
        def check_folder(f):
            if not Path.is_dir(f):
                mkdir(f)

        check_folder(XDG_CONFIG)

        dooit = XDG_CONFIG / "dooit"
        check_folder(dooit)

        if data := environ.get("XDG_DATA_HOME"):
            data_path = Path(data)
        else:
            local = HOME / ".local"
            check_folder(local)
            data_path = local / "share"
            check_folder(data_path)

        dooit_data = data_path / "dooit"
        check_folder(dooit_data)

        self.todo_yaml = dooit_data / "todo.yaml"
        if not Path.is_file(self.todo_yaml):
            with open(self.todo_yaml, "w") as f:
                yaml.safe_dump(dict(), f)
