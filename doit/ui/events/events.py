from textual import events
from textual.events import Event


class DateKeypress(Event):
    def __init__(self, sender, key: events.Key) -> None:
        super().__init__(sender)
        self.key = key


class UrgencyKeypress(Event):
    def __init__(self, sender, key: events.Key) -> None:
        super().__init__(sender)
        self.key = key


class MenuOptionChange(Event):
    def __init__(self, sender, option: str) -> None:
        super().__init__(sender)
        self.option = option
