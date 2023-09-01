from rich.console import RenderableType
from rich.text import Text, TextType
from .utils import StatusMiddle


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
