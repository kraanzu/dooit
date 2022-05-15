from datetime import datetime


class Task:
    """
    A task class to store data of the task
        PENDING
        COMPLETED
        OVERDUE
    """

    def __init__(
        self,
        name: str | None = None,
        priority: int = 1,
        due: str | None = None,
    ) -> None:
        self.name = name
        self.priority = priority
        self.tags = []
        self.status = "PENDING"
        self.due = due
        self.created = datetime.now().time().strftime("on %D at %T")
        self.last_modified = self.created

