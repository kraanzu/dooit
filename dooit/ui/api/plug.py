from functools import partial
import sys
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Callable, List, Type
from platformdirs import user_config_dir
from textual.css.query import NoMatches

from dooit.ui.api.events import DOOIT_EVENT_ATTR, DOOIT_TIMER_ATTR
from dooit.ui.events.events import DooitEvent, Startup
from .loader import load_dir, load_file

if TYPE_CHECKING:  # pragma: no cover
    from dooit.ui.api.dooit_api import DooitAPI


if getattr(sys, "frozen", False):
    BASE_PATH = Path(sys._MEIPASS) / "dooit"  # pragma: no cover (binary pkg)
else:
    BASE_PATH = Path(__file__).parent.parent.parent

MAIN_FOLDER = "dooit_v3"
CONFIG_FOLDER = Path(user_config_dir(MAIN_FOLDER))
DEFAULT_CONFIG = BASE_PATH / "utils" / "default_config.py"


class PluginManager:
    def __init__(self, api: "DooitAPI") -> None:
        self.events: defaultdict[Type[DooitEvent], List[Callable]] = defaultdict(list)
        self.timers: defaultdict[float, List[Callable]] = defaultdict(list)
        self.api = api
        self.app = api.app

    def scan(self):
        load_file(self, DEFAULT_CONFIG)
        load_dir(self, CONFIG_FOLDER)

    def kickstart_timers(self):
        for funcs in self.timers.values():
            for obj in funcs:
                obj()

    def _update_dooit_value(self, obj, *params):
        res = obj(self.api, *params)
        setattr(obj, "__dooit_value", res)

        try:
            if bar := getattr(self.app, "bar", None):
                bar.refresh()
        except NoMatches:
            pass

    def on_event(self, event: DooitEvent):
        for obj in self.events[event.__class__]:
            self._update_dooit_value(obj, event)

    def _register_events(self, events: List[Type[DooitEvent]], obj: Callable):
        for event in events:
            self.events[event].append(obj)

    def _register_timer(self, obj: Callable):
        self._register_events([Startup], obj)

        if interval := getattr(obj, DOOIT_TIMER_ATTR, None):
            func = partial(self._update_dooit_value, obj)
            self.timers[interval].append(func)

    def register(self, obj):
        if event := getattr(obj, DOOIT_EVENT_ATTR, None):
            self._register_events(event, obj)

        if getattr(obj, DOOIT_TIMER_ATTR, None):
            self._register_timer(obj)
