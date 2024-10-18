from typing import TYPE_CHECKING
from .formatter_store import FormatterStore

if TYPE_CHECKING:
    from dooit.ui.tui import Dooit


class ModelFormatterBase:
    def __init__(self, app: "Dooit") -> None:
        self.app = app
        self.setup_formatters()

    def get_formatter_store(self) -> FormatterStore:
        return FormatterStore(self.trigger, self.app)

    def setup_formatters(self) -> None:  # pragma: no cover
        pass

    def trigger(self) -> None:  # pragma: no cover
        pass
