from collections.abc import Callable
from typing import Any, Dict, Optional, Tuple
from rich.console import JustifyMethod, RenderableType
from rich.text import Text


class Widget:
    """
    Renderable Widget class for status bar
    """

    def __init__(
        self,
        func: Callable,
        width: Optional[int] = None,
        expand: bool = False,
        justify: JustifyMethod = "center",
    ) -> None:
        self.func = func
        self.width = width
        self.expand = expand
        self.justify = justify

    def render(self) -> Tuple[RenderableType, Dict[str, Any]]:
        renderable = self.func()
        if isinstance(renderable, str):
            renderable = Text.from_markup(renderable)

        params: Dict[str, Any] = {
            "justify": self.justify,
        }
        if self.expand:
            params["ratio"] = 1
        else:
            params["width"] = self.width or len(renderable)

        return renderable, params
