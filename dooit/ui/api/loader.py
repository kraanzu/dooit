import importlib.util
import sys
from typing import TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:  # pragma: no cover
    from .plug import PluginManager


def register(api: "PluginManager", path: Path) -> None:
    spec = importlib.util.spec_from_file_location("", path)

    if spec and spec.loader:
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        for obj in vars(foo).values():
            api.register(obj)


def load_file(api: "PluginManager", path: Path) -> bool:
    if not path.exists():
        return False

    if path.suffix == ".py":
        register(api, path)

    return True


def load_dir(api: "PluginManager", path: Path) -> bool:
    # allows users to import from the directory
    sys.path.append(str(path.resolve()))

    if not path.exists():
        return False

    for file in path.iterdir():
        if file.is_dir():
            return load_dir(api, file)

        load_file(api, file)

    return True
