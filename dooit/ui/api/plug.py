from collections import defaultdict
from pathlib import Path
from typing import Callable
from appdirs import user_config_dir, user_data_dir
from .loader import load_dir


CONFIG_FOLDER = Path(user_config_dir("dooit"))
PLUGINS_FOLDER = Path(user_data_dir("dooit")) / "plugins"


class PluginManager:
    def __init__(self) -> None:
        self.events = defaultdict(list)

    def scan(self):
        load_dir(self, CONFIG_FOLDER)
        load_dir(self, PLUGINS_FOLDER)

    def _register_event(self, event: str, obj: Callable):
        self.events[event].append(obj)

    def register(self, name, obj):
        event = getattr(obj, "__dooit_event")
        self._register_event(event, obj)
