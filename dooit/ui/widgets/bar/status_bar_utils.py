from textual.widget import Widget
from textual import work
from rich.console import RenderableType
from rich.text import Text, TextType
from dooit.ui.events.events import ChangeStatus

from dooit.ui.widgets.search_menu import SearchMenu


from ..simple_input import Input
from ..bar_widget import BarWidget
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
