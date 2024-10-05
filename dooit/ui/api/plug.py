import sys
from collections import defaultdict
from pathlib import Path
from typing import Callable, List
from platformdirs import user_config_dir

from dooit.ui.api.events import DOOIT_EVENT_ATTR
from dooit.ui.events.events import DooitEvent
from .loader import load_dir, load_file


if getattr(sys, "frozen", False):
    BASE_PATH = Path(sys._MEIPASS) / "dooit"  # pragma: no cover (binary pkg)
else:
    BASE_PATH = Path(__file__).parent.parent.parent

MAIN_FOLDER = "dooit_v3"
CONFIG_FOLDER = Path(user_config_dir(MAIN_FOLDER))
DEFAULT_CONFIG = BASE_PATH / "utils" / "default_config.py"


class PluginManager:
    def __init__(self) -> None:
        self.events = defaultdict(list)

    def scan(self):
        load_file(self, DEFAULT_CONFIG)
        load_dir(self, CONFIG_FOLDER)

    def _register_events(self, events: List[DooitEvent], obj: Callable):
        for event in events:
            self.events[event].append(obj)

    def register(self, obj):
        if event := getattr(obj, DOOIT_EVENT_ATTR, None):
            self._register_events(event, obj)
