from enum import Enum
from rich.style import Style
from rich.text import Text
from rich.console import Console


class LogLevel(Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class CliLogger:
    def __init__(self) -> None:
        self.console = Console()
        self.print = self.console.print

    def _log(self, level: LogLevel, *messages: str) -> None:
        icon = {
            LogLevel.SUCCESS: "+",
            LogLevel.INFO: "+",
            LogLevel.WARN: "-",
            LogLevel.ERROR: "!",
        }[level]

        color = {
            LogLevel.SUCCESS: "green",
            LogLevel.INFO: "blue",
            LogLevel.WARN: "yellow",
            LogLevel.ERROR: "red",
        }[level]

        message = Text.assemble(
            Text(f"[{icon}]", style=Style(color=color, bold=True)),
            Text(),
            *[Text.from_markup(f" {message}", style=color) for message in messages],
        )

        self.print(message)

    def info(self, *messages: str) -> None:
        self._log(LogLevel.INFO, *messages)

    def warn(self, *messages: str) -> None:
        self._log(LogLevel.WARN, *messages)

    def error(self, *messages: str) -> None:
        self._log(LogLevel.ERROR, *messages)

    def success(self, *messages: str) -> None:
        self._log(LogLevel.SUCCESS, *messages)


logger = CliLogger()
