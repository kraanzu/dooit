from datetime import datetime
from dooit.ui.api import events, DooitAPI
from dooit.ui.api.components import TodoComponent, WorkspaceComponent


def due_formatter(todo):
    due = todo.due
    if due == "none":
        due = None

    due = due or datetime.now()
    return due.strftime("Now: %H:%M")


@events.startup
def key_setup(api: DooitAPI):
    api.set_key_normal("tab", api.switch_focus)
    api.set_key_normal("j", api.move_down)
    api.set_key_normal("k", api.move_up)
    api.set_key_normal("i", api.edit_description)
    api.set_key_normal("a", api.add_sibling)

    api.set_workspace_layout([WorkspaceComponent.description])

    api.set_todo_layout(
        [
            TodoComponent.description,
            (TodoComponent.due, due_formatter),
        ]
    )
