from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..tui import Dooit


class DooitAPI:
    def __init__(self, app: "Dooit") -> None:
        self.app = app

    def handle_key(self, key: str) -> None:
        exit()
