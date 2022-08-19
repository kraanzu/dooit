from typing import Optional
from dooit.utils import Urgency
from string import printable as chars
from random import choice


def generate_uuid() -> str:
    """
    Generates a random id for entries
    """
    return "".join([choice(chars) for _ in range(32)])


class Todo:
    """
    Singlw todo Manager class
    """

    def __init__(
        self,
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Optional[Urgency] = None,
    ) -> None:
        self.about = about
        self.due = due
        self.urgency = urgency or Urgency.D
        self.id = generate_uuid()

    def edit(
        self,
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Optional[Urgency] = None,
    ) -> None:
        if about:
            self.about = about
        if due:
            self.due = due
        if urgency:
            self.urgency = urgency
