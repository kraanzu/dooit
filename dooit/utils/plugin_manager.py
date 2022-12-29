import os
from collections import deque
import importlib.util
from inspect import isclass
from threading import Thread
from typing import Any, Dict, List

from dooit.api.manager import Manager
from .plugin import Plugin
from .parser import PLUGINS_PATH


def get_vars(path: str) -> Dict[str, Any]:
    spec = importlib.util.spec_from_file_location("plug", path)
    if spec and spec.loader:
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        return vars(foo)

    return {}


def get_plugins(path: str, manager) -> List[Plugin]:
    arr = []
    for i in get_vars(path).values():
        if isclass(i) and issubclass(i, Plugin):
            arr.append(i(manager))

    return arr


class PluginManager:
    def __init__(self, manager: Manager) -> None:
        plugins = []
        for directory, _, filelist in os.walk(PLUGINS_PATH):
            for file in filelist:
                if file.endswith(".py"):
                    path = os.path.join(directory, file)
                    plugins.extend(get_plugins(path, manager))

        self.queue = deque(plugins)
        self.queue_exit = []

    def start(self):
        while self.queue:
            plugin: Plugin = self.queue.popleft()

            if plugin.ready:
                plugin.running = False
                while plugin.manager.is_locked():
                    pass

                plugin.manager.lock()
                res = plugin.run()
                plugin.manager.unlock()
                plugin.manager.enable_force_refresh()
                plugin.commit()

                if res:
                    plugin.ready = False
                    self.queue.append(plugin)
                else:
                    self.queue_exit.append(plugin)

            else:
                if not plugin.running:
                    Thread(target=plugin.pre_process, daemon=True).start()
                    plugin.running = True

                self.queue.append(plugin)

    def cleanup(self):
        while self.queue_exit:
            plugin: Plugin = self.queue_exit.pop()
            while plugin.manager.is_locked():
                pass

            plugin.manager.lock()
            plugin.run_on_exit()
            plugin.manager.unlock()
            plugin.manager.enable_force_refresh()
            plugin.commit()
