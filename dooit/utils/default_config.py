from datetime import datetime
from dooit.ui.api import events, DooitAPI
from dooit.ui.api.widgets import TodoWidget, WorkspaceWidget
from dooit.ui.widgets.bars import StatusBarWidget
from rich.text import Text


def get_mode():
    mode = " NORMAL "
    return Text(f" {mode} ", style="black on white")


def spacer():
    return Text(" ")


bar_widgets = [
    StatusBarWidget(spacer),
    StatusBarWidget(get_mode),
]


def due_formatter(due, _):
    if due == "none":
        due = None

    due = due or datetime.now()
    return due.strftime("%H:%M")


@events.startup
def key_setup(api: DooitAPI):
    api.keys.set_normal("tab", api.switch_focus)
    api.keys.set_normal("j", api.move_down)
    api.keys.set_normal("k", api.move_up)
    api.keys.set_normal("i", api.edit_description)
    api.keys.set_normal("d", api.edit_due)
    api.keys.set_normal("a", api.add_sibling)
    api.keys.set_normal("z", api.toggle_expand)
    api.keys.set_normal("Z", api.toggle_expand_parent)
    api.keys.set_normal("g", api.go_to_top)
    api.keys.set_normal("G", api.go_to_bottom)
    api.keys.set_normal("A", api.add_child_node)
    api.keys.set_normal("J", api.shift_down)
    api.keys.set_normal("K", api.shift_up)
    api.keys.set_normal("x", api.remove_node)
    api.keys.set_normal("/", api.start_search)
    api.keys.set_normal("ctrl+s", api.start_sort)

    api.layouts.workspace_layout = [WorkspaceWidget.description]
    api.layouts.todo_layout = [TodoWidget.description, TodoWidget.due]

    api.set_bar(bar_widgets)
