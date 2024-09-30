from dooit.api import Todo, Workspace
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
    if not due or due == "none":
        return ""

    text = due.strftime("%Y-%m-%d")

    if due.hour:
        text += f" ({due.strftime('%H:%M')})"

    return text

def workspace_desc_formatter(desc: str, workspace: Workspace):
    text = desc

    if ws := workspace.workspaces:
        text += f" ({len(ws)})"

    return text

def todo_desc_formatter(desc: str, todo: Todo):
    text = desc

    if ts := todo.todos:
        text += f" ({len(ts)})"

    if r := todo.recurrence:
        text += f" !{r.days}d"

    return text


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

    api.formatter.workspaces.description.add(workspace_desc_formatter)
    api.formatter.todos.description.add(todo_desc_formatter)
    api.formatter.todos.due.add(due_formatter)

    api.set_bar(bar_widgets)
