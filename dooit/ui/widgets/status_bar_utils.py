from textual.widget import Widget
from rich.console import RenderableType
from rich.text import Text, TextType
from .simple_input import Input
from .bar_widget import BarWidget
from dooit.utils.conf_reader import Config

BG = Config().get("BACKGROUND")
bar = Config().get("bar")


class AutoHorizontal(Widget):
    DEFAULT_CSS = """
    AutoHorizontal {
        layout: horizontal;
        max-height: 1;
        width: auto;
    }
    """


class StatusMiddle(Widget):
    DEFAULT_CSS = f"""
    StatusMiddle {{
        background: {BG} 10%;
    }}
    """


class StatusMessage(StatusMiddle):
    msg = Text()

    def set_message(self, msg: TextType):
        if isinstance(msg, str):
            msg = Text.from_markup(msg)

        self.msg = msg
        self.refresh()

    def clear(self):
        self.set_message("")

    def render(self) -> RenderableType:
        return self.msg


class Searcher(StatusMiddle, Input):
    DEFAULT_CSS = f"""
    Searcher {{
        background: {BG};
        padding-left: 1;
    }}
    """

    def clear(self) -> None:
        super().clear()

    async def keypress(self, key: str) -> None:
        if key == "escape":
            return await self.app.query_one("StatusBar").stop_search()

        await super().keypress(key)

        focused = self.app.query(".focus").first()
        await focused.apply_filter(self.value)


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
        self.run_worker(self.refresh_value, exclusive=True)
        self.refresh(layout=True)

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
