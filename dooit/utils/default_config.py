from datetime import datetime
from dooit.ui.api import events, DooitAPI
from dooit.ui.api.components import TodoComponent, WorkspaceComponent
from dooit.ui.widgets import BarWidget
from rich.text import Text


def get_mode():
    mode = " NORMAL "
    return Text(f" {mode} ", style="black on white")


def spacer():
    return Text(" ")


bar_widgets = [
    BarWidget(spacer),
    BarWidget(get_mode),
]


def due_formatter(due, _):
    if due == "none":
        due = None

    due = due or datetime.now()
    return due.strftime("%H:%M")


@events.startup
def key_setup(api: DooitAPI):
    api.set_key_normal("tab", api.switch_focus)
    api.set_key_normal("j", api.move_down)
    api.set_key_normal("k", api.move_up)
    api.set_key_normal("i", api.edit_description)
    api.set_key_normal("a", api.add_sibling)
    api.set_key_normal('z', api.toggle_expand)
    api.set_key_normal('Z', api.toggle_expand_parent)
    api.set_key_normal("g", api.go_to_top)
    api.set_key_normal("G", api.go_to_bottom)

    api.set_workspace_layout([WorkspaceComponent.description])

    api.set_todo_layout(
        [
            TodoComponent.description,
            (TodoComponent.due, due_formatter),
        ]
    )

    api.set_bar(bar_widgets)
