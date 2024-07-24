from enum import Enum
from typing import List, Tuple, Callable, Union


class WorkspaceComponent(Enum):
    description = "description"


class TodoComponent(Enum):
    description = "description"
    due = "due"
    urgency = "urgency"
    recurrence = "recurrence"
    status = "status"
    effort = "effort"


WorkspaceLayout = List[Union[Tuple[WorkspaceComponent, Callable], WorkspaceComponent]]
TodoLayout = List[Union[Tuple[TodoComponent, Callable], TodoComponent]]
