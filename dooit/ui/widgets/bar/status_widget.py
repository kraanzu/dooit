from textual.widget import Widget
from textual import work
from rich.console import RenderableType
from rich.text import Text
from ..bar_widget import BarWidget


class StatusWidget(Widget):
    DEFAULT_CSS = """
    StatusWidget {
        width: auto;
        max-height: 1;
    }
    """
    _value = Text()

    def __init__(self, widget: BarWidget):
        super().__init__()

        if not isinstance(widget, BarWidget):
            exit(
                "The method of creating bar widgets was changed."
                + "\n"
                + "Please refer to this: https://www.google.com"
            )

        self.widget = widget
        self.refresh_value()

        if widget.delay > 0:
            self.set_interval(widget.delay, self.redraw)

    def redraw(self):
        self.refresh_value()
        self.refresh(layout=True)

    @work(exclusive=True)
    def refresh_value(self):
        try:
            params = self.app.query_one("StatusBar").get_params()
            self._value = self.widget.get_value(**params)
        except:
            pass

    def render(self) -> RenderableType:
        res = self._value
        self.styles.min_width = len(res)
        return res
