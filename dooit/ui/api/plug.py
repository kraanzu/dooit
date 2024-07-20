from collections import defaultdict
from pathlib import Path
from typing import Callable
from appdirs import user_config_dir
from .loader import load_dir, load_file

MAIN_FOLDER = "dooit_v3"

CONFIG_FOLDER = Path(user_config_dir(MAIN_FOLDER))
PLUGINS_FOLDER = CONFIG_FOLDER / "plugins"
DEFAULT_CONFIG = Path(__file__).parent.parent.parent / "utils" / "default_config.py"


class PluginManager:
    def __init__(self) -> None:
        self.events = defaultdict(list)

    def scan(self):
        load_dir(self, CONFIG_FOLDER)
        load_dir(self, PLUGINS_FOLDER)
        load_file(self, DEFAULT_CONFIG)

    def _register_event(self, event: str, obj: Callable):
        self.events[event].append(obj)

    def register(self, name, obj):
        event = getattr(obj, "__dooit_event")
        self._register_event(event, obj)
