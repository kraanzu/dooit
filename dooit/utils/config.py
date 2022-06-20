import os
import yaml
from pathlib import Path
from os import environ

HOME = Path.home()
XDG_CONFIG = Path(environ.get("XDG_CONFIG_HOME") or (HOME / ".config"))
DOOIT = XDG_CONFIG / "dooit"
CONFIG = DOOIT / "config.yaml"

SAMPLE = Path(__file__).parent.absolute() / "example_config.yaml"


class Key:
    def __init__(self, keybinds: dict[str, list[str]]):
        # for i, j in keybinds.items():
        #     setattr(self, i, j)

        self.move_to_top = keybinds["move_to_top"]
        self.move_to_bottom = keybinds["move_to_bottom"]
        self.move_down = keybinds["move_down"]
        self.shift_down = keybinds["shift_down"]
        self.move_up = keybinds["move_up"]
        self.shift_up = keybinds["shift_up"]
        self.edit_node = keybinds["edit_node"]
        self.edit_date = keybinds["edit_date"]
        self.toggle_complete = keybinds["toggle_complete"]
        self.yank_todo = keybinds["yank_todo"]
        self.toggle_expand = keybinds["toggle_expand"]
        self.toggle_expand_parent = keybinds["toggle_expand_parent"]
        self.remove_node = keybinds["remove_node"]
        self.add_sibling = keybinds["add_sibling"]
        self.add_child = keybinds["add_child"]
        self.spawn_sort_menu = keybinds["spawn_sort_menu"]
        self.start_search = keybinds["start_search"]
        self.select_node = keybinds["select_node"]
        self.move_focus_to_menu = keybinds["move_focus_to_menu"]
        self.show_help = keybinds["show_help"]
        self.increase_urgency = keybinds["increase_urgency"]
        self.decrease_urgency = keybinds["decrease_urgency"]


class Config:
    def __init__(self) -> None:
        self.check_files()

    def make_new_config(self):
        with open(SAMPLE, "r") as f:
            with open(CONFIG, "w") as stream:
                stream.write(f.read())

    def check_files(self):
        if not DOOIT.is_dir():
            os.mkdir(DOOIT)

        if not CONFIG.is_file():
            self.make_new_config()

        try:
            self.keybinds = self.load_keybindings()
            self.keys = Key(self.keybinds)
        except:
            self.make_new_config()
            self.keybinds = self.load_keybindings()
            self.keys = Key(self.keybinds)

    def load_config(self, part: str = "main") -> dict:
        with open(CONFIG, "r") as stream:
            try:
                return yaml.safe_load(stream)[part]
            except yaml.YAMLError:
                self.make_new_config()
                return self.load_config(part)

    def load_keybindings(self) -> dict[str, list[str]]:
        keybinds = self.load_config("keybindings")
        for key in list(keybinds.keys()):
            bind = keybinds[key]
            if isinstance(bind, str):
                keybinds[key] = [bind]

        return keybinds


conf = Config()
