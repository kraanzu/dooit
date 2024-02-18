import appdirs
import msgpack
import os
import yaml
from typing import Dict
from pathlib import Path
from os import makedirs

XDG_CONFIG = Path(appdirs.user_config_dir("dooit"))
XDG_DATA = Path(appdirs.user_data_dir("dooit"))
TODO_DATA = XDG_DATA / "todo.dat"


class Parser:
    """
    Parser class to manage and parse dooit's config and data
    """

    @property
    def last_modified(self) -> float:
        return os.stat(TODO_DATA).st_mtime

    def __init__(self) -> None:
        self.check_files()

    def save(self, data) -> None:
        """
        Save the todos to data file
        """

        with open(TODO_DATA, "wb") as stream:
            stream.write(msgpack.packb(data, use_bin_type=True))

    def load(self) -> Dict:
        """
        Retrieves the todos from data file
        """

        with open(TODO_DATA, "rb") as stream:
            data = msgpack.unpackb(stream.read(), raw=False)

        return data

    def check_files(self) -> None:
        """
        Checks if all the files and folders are present
        to avoid any errors
        """

        makedirs(XDG_CONFIG, exist_ok=True)
        makedirs(XDG_DATA, exist_ok=True)

        self.config_file = XDG_CONFIG / "config.py"
        self.todo_data_yaml = XDG_DATA / "todo.yaml"

        if Path.is_file(self.todo_data_yaml):
            self.migrate_to_msgpack()
        elif not Path.is_file(TODO_DATA):
            self.save(dict())

        if not Path.is_file(self.config_file):
            with open(self.config_file, "w") as _:
                pass

    def migrate_to_msgpack(self):
        with open(self.todo_data_yaml, "r") as stream:
            self.save(yaml.safe_load(stream))

        os.remove(self.todo_data_yaml)
