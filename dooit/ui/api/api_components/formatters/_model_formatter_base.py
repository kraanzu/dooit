from textual.app import App


class ModelFormatterBase:
    def __init__(self, app: App) -> None:
        self.app = app
        self.setup_formatters()

    def setup_formatters(self) -> None: # pragma: no cover
        pass

    def trigger(self) -> None: # pragma: no cover
        pass
