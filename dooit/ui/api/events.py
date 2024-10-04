from typing import Callable, Type
from dooit.ui.events.events import *  # noqa


class Hook:
    def __init__(self, event: Type[DooitEvent]):
        self.event = event

    def __call__(self, func: Callable):
        setattr(func, "__dooit_event", self.event)
        return func


startup = Hook(Startup)
shutdown = Hook(ShutDown)
mode_changed = Hook(ModeChanged)

workspace_selected = Hook(WorkspaceSelected)
workspace_description_changed = Hook(WorkspaceDescriptionChanged)

todo_selected = Hook(TodoSelected)
todo_description_changed = Hook(TodoDescriptionChanged)
todo_due_changed = Hook(TodoDueChanged)
todo_status_changed = Hook(TodoStatusChanged)
todo_urgency_changed = Hook(TodoUrgencyChanged)
todo_effort_changed = Hook(TodoEffortChanged)
todo_recurrence_changed = Hook(TodoRecurrenceChanged)
