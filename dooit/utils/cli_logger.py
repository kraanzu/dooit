from enum import Enum
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
            Text(f"[{icon}]"),
            *[Text(f" {message}", style=color) for message in messages],
        )

        self.print(message)

    def log_info(self, *messages: str) -> None:
        self._log(LogLevel.INFO, *messages)

    def log_warn(self, *messages: str) -> None:
        self._log(LogLevel.WARN, *messages)

    def log_error(self, *messages: str) -> None:
        self._log(LogLevel.ERROR, *messages)

    def log_success(self, *messages: str) -> None:
        self._log(LogLevel.SUCCESS, *messages)


logger = CliLogger()
