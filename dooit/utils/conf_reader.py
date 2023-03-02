from importlib.machinery import ModuleSpec
import importlib.util
from os import path
from typing import Any, Dict, Optional
import appdirs
import sys

sys.path.append(appdirs.user_config_dir("dooit"))
user_config = path.join(appdirs.user_config_dir("dooit"), "config.py")
default_config = path.join(path.dirname(__file__), "default_config.py")

default_spec = importlib.util.spec_from_file_location("default_config", default_config)
if path.isfile(user_config):
    user_spec = importlib.util.spec_from_file_location("user_config", user_config)
else:
    user_spec = default_spec


def get_vars(spec: Optional[ModuleSpec]) -> Dict[str, Any]:
    if spec and spec.loader:
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        return vars(foo)

    return {}


def combine_into(d: dict, to: dict) -> None:
    for k, v in d.items():
        if isinstance(v, dict):
            combine_into(v, to.setdefault(k, {}))
        else:
            to[k] = v


class Config:
    def __init__(self) -> None:
        self._d = {}
        self.update()

    def update(self):
        for i in [default_spec, user_spec]:
            combine_into(get_vars(i), self._d)

    def get(self, var: str) -> Any:
        return self._d[var]
