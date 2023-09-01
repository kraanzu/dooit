from rich.console import RenderableType
from rich.text import TextType
from textual.widget import Widget
from textual.widgets import Label


class Pointer(Widget):
    """
    Pointer Widget to show current selected widget
    """

    DEFAULT_CSS = """
    Pointer {
        padding-left: 1;
        padding-right: 1;
        width: auto;
    }
    """

    _show = False

    def __init__(self, symbol: TextType):
        super().__init__()
        self.symbol = symbol

    def show(self):
        self._show = True
        self.refresh()

    def hide(self):
        self._show = False
        self.refresh()

    def render(self) -> RenderableType:
        return self.symbol if self._show else " " * len(self.symbol)


class Padding(Label):
    DEFAULT_CSS = """
    Padding {
        height: 1;
        width: auto;
    }
    """

    def __init__(self, width):
        self.padding_width = width
        super().__init__()

    def render(self) -> RenderableType:
        return "  " * self.padding_width
