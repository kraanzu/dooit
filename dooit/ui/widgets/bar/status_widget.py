from typing import Callable, Tuple
from textual.widget import Widget
from textual import work
from inspect import getfullargspec as get_args
from rich.console import RenderableType
from rich.text import Text


BarWidgetConfig = Tuple[Callable, float]


class StatusWidget(Widget):
    """
    Custom Widgets for status bar!
    """

    DEFAULT_CSS = """
    StatusWidget {
        width: auto;
        max-height: 1;
    }
    """
    _value = Text()

    def __init__(self, config: BarWidgetConfig):
        super().__init__()

        if not isinstance(config, tuple):
            if isinstance(config, Callable):
                func = (config, 1)
            else:
                func = (lambda: str(config), 1)
        else:
            if len(config) == 1:
                func = (config[0], 1)
            else:
                func = config

        self.func = func[0]
        delay = func[1]

        self.refresh_value()

        if delay > 0:
            self.set_interval(delay, self.redraw)

    def redraw(self):
        self.refresh_value()
        self.refresh(layout=True)

    def get_value(self, **kwargs) -> Text:
        args = get_args(self.func).args
        value = self.func(**{i: kwargs[i] for i in args})
        if isinstance(value, str):
            value = Text.from_markup(value)

        return value

    @work(exclusive=True, thread=True)
    def refresh_value(self):
        from dooit.ui.widgets.bar.status_bar import StatusBar

        try:
            params = self.app.query_one(StatusBar).get_params()
            self._value = self.get_value(**params)
        except Exception:
            pass

    def render(self) -> RenderableType:
        res = self._value
        self.styles.min_width = len(res)
        return res
