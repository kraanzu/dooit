from .model import Model, T
from .manager import Manager, manager
from .todo import Todo
from .workspace import Workspace
from threading import Thread


def deal_with_dateparser():
    # HACK: Need to do this as
    # dateparser slows down on first incorrect parsing :(

    import dateparser

    dateparser.parse("none")


Thread(target=deal_with_dateparser, daemon=True).start()

__all__ = ["Model", "Manager", "Todo", "Workspace", "T", "manager"]
