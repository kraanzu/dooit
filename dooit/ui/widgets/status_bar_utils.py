from textual.widget import Widget
from textual import work
from rich.console import RenderableType
from rich.text import Text, TextType
from dooit.ui.events.events import ChangeStatus, StopSearch

from dooit.ui.widgets.search_menu import SearchMenu


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

    async def on_mount(self):
        from dooit.ui.widgets.status_bar import StatusBar

        self.app.query_one(StatusBar).set_status("SEARCH")

    async def on_unmount(self):
        from dooit.ui.widgets.status_bar import StatusBar

        self.app.query_one(StatusBar).set_status("NORMAL")

    async def keypress(self, key: str) -> None:
        if key == "escape":
            self.post_message(StopSearch())
            return

        if key == "enter":
            self.post_message(ChangeStatus("NORMAL"))

        await super().keypress(key)
        self.app.query_one(SearchMenu).apply_filter(self.value)


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
