from enum import Enum
from typing import List, Tuple, Callable


class WorkspaceComponent(Enum):
    description = "description"


class TodoComponent(Enum):
    description = "description"
    due = "due"
    urgency = "urgency"
    recurrence = "recurrence"
    status = "status"
    effort = "effort"


WorkspaceLayout = List[Tuple[WorkspaceComponent, Callable]]
TodoLayout = List[Tuple[TodoComponent, Callable]]
