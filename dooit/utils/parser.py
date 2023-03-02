import appdirs
import yaml
import os
from typing import Dict
from pathlib import Path
from os import mkdir

XDG_CONFIG = Path(appdirs.user_config_dir("dooit"))
XDG_DATA = Path(appdirs.user_data_dir("dooit"))


class Parser:
    """
    Parser class to manage and parse dooit's config and data
    """

    @property
    def last_modified(self) -> float:
        return os.stat(self.todo_yaml).st_mtime

    def __init__(self) -> None:
        self.check_files()

    def save(self, data):
        """
        Save the todos to data file
        """

        with open(self.todo_yaml, "w") as stream:
            yaml.safe_dump(data, stream, sort_keys=False)

    def load(self) -> Dict:
        """
        Retrieves the todos from data file
        """

        with open(self.todo_yaml, "r") as stream:
            data = yaml.safe_load(stream)

        return data

    def check_files(self) -> None:
        """
        Checks if all the files and folders are present
        to avoid any errors
        """

        def check_folder(f: Path):
            if not Path.is_dir(f):
                mkdir(f)

        check_folder(XDG_CONFIG)
        check_folder(XDG_DATA)

        self.todo_yaml = XDG_DATA / "todo.yaml"
        self.config_file = XDG_CONFIG / "config.py"

        if not Path.is_file(self.todo_yaml):
            with open(self.todo_yaml, "w") as f:
                yaml.safe_dump(dict(), f)

        if not Path.is_file(self.config_file):
            with open(self.config_file, "w") as f:
                pass
