from typing import Callable, Union
from inspect import getfullargspec as get_args
from rich.console import RenderableType
from rich.text import Text, TextType
from textual.app import ComposeResult
from textual.widget import Widget
from dooit.utils.conf_reader import Config
from dooit.api import manager
from ..events import StatusType

bar = Config().get("bar")
BG = Config().get("BACKGROUND")


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


class StatusWidget(Widget):
    DEFAULT_CSS = """
    StatusWidget {
        width: auto;
        max-height: 1;
    }
    """
    _value = Text()

    def __init__(self, func: Union[Callable, TextType], classes: str = ""):
        super().__init__(classes=classes)
        self.func = func
        self.refresh_value()
        self.set_interval(0.1, self.redraw)

    def redraw(self):
        self.run_worker(self.refresh_value, exclusive=True)
        self.refresh(layout=True)

    def refresh_value(self):
        if isinstance(self.func, Callable):
            args = get_args(self.func).args
            params = self.app.query_one(StatusBar).get_params()
            res = self.func(**{i: params[i] for i in args})
        else:
            res = self.func

        if not isinstance(res, Text):
            res = Text.from_markup(str(res))

        self._value = res

    def render(self) -> RenderableType:
        res = self._value
        self.styles.min_width = len(res)
        return res


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


class StatusBar(Widget):
    """
    A status bar widget for showing messages and looks :)
    """

    DEFAULT_CSS = """
        StatusBar {
            column-span: 2;
            max-height: 1;
            layout: horizontal;
        }
    """

    def __init__(self) -> None:
        super().__init__()
        self.status = "NORMAL"

    def set_message(self, message: TextType = "") -> None:
        self.query_one(StatusMessage).set_message(message)

    def clear_message(self) -> None:
        self.query_one(StatusMessage).clear()

    def set_status(self, status: StatusType) -> None:
        self.status = status
        self.refresh()

    def get_params(self):
        return {
            "status": self.status,
            "manager": manager,
        }

    def compose(self) -> ComposeResult:
        yield AutoHorizontal(*[StatusWidget(i) for i in bar["A"]], classes="dock-left")
        yield StatusMessage()
        yield AutoHorizontal(*[StatusWidget(i) for i in bar["C"]], classes="dock-right")
