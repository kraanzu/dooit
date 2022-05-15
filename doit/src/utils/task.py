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
        urgency: int = 1,
        due: str | None = None,
    ) -> None:
        self.name = name
        self.urgency = urgency
        self.tags = []
        self.status = "PENDING"
        self.due = due

