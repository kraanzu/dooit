from enum import Enum


class WorkspaceComponent(Enum):
    description = "description"


class TodoComponent(Enum):
    description = "description"
    due = "due"
    urgency = "urgency"
    recurrence = "recurrence"
    status = "status"
    effort = "effort"
