from importlib.machinery import ModuleSpec
from os import path
from typing import Any, Dict, Optional
import appdirs
import importlib.util

user_config = path.join(appdirs.user_config_dir("dooit"), "config.py")
default_config = path.join(path.dirname(__file__), "default_config.py")

user_spec = importlib.util.spec_from_file_location("user_config", user_config)
default_spec = importlib.util.spec_from_file_location("default_config", default_config)


def get_vars(spec: Optional[ModuleSpec]) -> Dict[str, Any]:
    if spec and spec.loader:
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        return vars(foo)

    return {}


class Config:
    def __init__(self) -> None:
        self.update()

    def update(self):
        self._d = get_vars(user_spec) | get_vars(default_spec)

    def get(self, var: str) -> Any:
        return self._d[var]
