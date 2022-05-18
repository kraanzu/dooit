from textual.message import Message, MessageTarget

class Keystroke(Message, bubble=True):
    def __init__(self, sender: MessageTarget, key: str) -> None:
        super().__init__(sender)
        self.key = key


class UrgencyKeypress(Message, bubble=True):
    def __init__(self, sender: MessageTarget, key: str) -> None:
        super().__init__(sender)
        self.key = key


class MenuOptionChange(Message, bubble=True):
    def __init__(self, sender: MessageTarget, option: str) -> None:
        super().__init__(sender)
        self.option = option
