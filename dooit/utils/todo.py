from typing import Optional
from dooit.utils import Urgency


class Todo:
    """
    Singlw todo Manager class
    """

    def __init__(
        self,
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Urgency = Urgency.D,
    ) -> None:
        self.about = about
        self.due = due
        self.urgency = urgency

    def edit(
        self,
        *,
        about: Optional[str] = None,
        due: Optional[str] = None,
        urgency: Urgency = Urgency.D,
    ) -> None:
        if about:
            self.about = about
        if due:
            self.due = due
        if urgency:
            self.urgency = urgency
