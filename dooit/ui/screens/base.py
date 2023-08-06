from textual.app import events
from textual.screen import Screen


class BaseScreen(Screen):
    PRINTABLE = (
        "0123456789"
        + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        + "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
    )

    def resolve_key(self, event: events.Key):
        return (
            event.character
            if (event.character and (event.character in self.PRINTABLE))
            else event.key
        )
