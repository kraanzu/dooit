from textual.app import App
from .formatter_store import FormatterStore


class ModelFormatterBase:
    def __init__(self, app: App) -> None:
        self.app = app
        self.setup_formatters()

    def get_formatter_store(self) -> FormatterStore:
        return FormatterStore(self.trigger)

    def setup_formatters(self) -> None:  # pragma: no cover
        pass

    def trigger(self) -> None:  # pragma: no cover
        pass
