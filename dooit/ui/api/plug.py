import os
import sys
from functools import partial
from collections import defaultdict
from pathlib import Path
from typing import TYPE_CHECKING, Callable, List, Type
from platformdirs import user_config_dir
from textual.css.query import NoMatches

from dooit.ui.api.event_handlers import DOOIT_EVENT_ATTR, DOOIT_TIMER_ATTR
from dooit.ui.api.events import DooitEvent
from .loader import load_file

if TYPE_CHECKING:  # pragma: no cover
    from dooit.ui.api.dooit_api import DooitAPI


if getattr(sys, "frozen", False):
    BASE_PATH = Path(sys._MEIPASS) / "dooit"  # pragma: no cover (binary pkg)
else:
    BASE_PATH = Path(__file__).parent.parent.parent

MAIN_FOLDER = "dooit"
CONFIG_FOLDER = Path(user_config_dir(MAIN_FOLDER))
DEFAULT_CONFIG = BASE_PATH / "utils" / "default_config.py"


def is_running_under_pytest() -> bool:
    return "PYTEST_CURRENT_TEST" in os.environ


class PluginManager:
    def __init__(self, api: "DooitAPI") -> None:
        self.events: defaultdict[Type[DooitEvent], List[Callable]] = defaultdict(list)
        self.timers: defaultdict[float, List[Callable]] = defaultdict(list)
        self.api = api
        self.app = api.app

    def scan(self):
        load_file(self, DEFAULT_CONFIG)
        if is_running_under_pytest():
            return

        load_file(self, CONFIG_FOLDER / "config.py")

    def _update_dooit_value(self, obj, *params):
        res = obj(self.api, *params)
        setattr(obj, "__dooit_value", res)

        try:
            if bar := getattr(self.app, "bar", None):
                bar.refresh()
        except NoMatches:
            pass

    def on_event(self, event: DooitEvent):
        matched_events = [
            e for e in self.events.keys() if issubclass(event.__class__, e)
        ]

        for e in matched_events:
            for obj in self.events[e]:
                self._update_dooit_value(obj, event)

    def _register_events(self, events: List[Type[DooitEvent]], obj: Callable):
        for event in events:
            self.events[event].append(obj)

    def _register_timer(self, obj: Callable):
        if interval := getattr(obj, DOOIT_TIMER_ATTR, None):
            func = partial(self._update_dooit_value, obj)
            func()
            self.api.app.set_interval(interval, func)

    def register(self, obj):
        if event := getattr(obj, DOOIT_EVENT_ATTR, None):
            return self._register_events(event, obj)

        if getattr(obj, DOOIT_TIMER_ATTR, None):
            return self._register_timer(obj)
