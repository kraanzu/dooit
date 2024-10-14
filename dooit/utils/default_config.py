from datetime import datetime
import os
from rich.style import Style
from dooit.api import Todo, Workspace
from dooit.ui.api import DooitAPI
from dooit.ui.api.events import subscribe, timer
from dooit.ui.api.widgets import TodoWidget, WorkspaceWidget
from dooit.ui.events.events import ModeChanged, Startup
from dooit.ui.widgets.bars import StatusBarWidget
from rich.text import Text
from functools import partial


@subscribe(ModeChanged)
def get_mode(api: DooitAPI, event: ModeChanged):
    theme = api.app.current_theme
    mode = event.mode

    MODES = {
        "NORMAL": theme.primary,
        "INSERT": theme.foreground_1,
    }

    return Text(
        f" {mode} ",
        style=Style(
            color=theme.background_1,
            bgcolor=MODES.get(mode, theme.primary),
        ),
    )


@timer(1)
def get_clock(api: DooitAPI, *_):
    theme = api.app.current_theme
    time = datetime.now().strftime("%H:%M:%S")
    return Text(
        f" {time} ",
        style=Style(
            color=theme.background_1,
            bgcolor=theme.secondary,
        ),
    )


@subscribe(Startup)
def get_user(api: DooitAPI, _: Startup):
    theme = api.app.current_theme
    try:
        username = os.getlogin()
    except OSError:
        uid = os.getuid()
        import pwd

        username = pwd.getpwuid(uid).pw_name
    return Text(
        f" {username} ",
        style=Style(
            color=theme.background_1,
            bgcolor=theme.secondary,
        ),
    )


# Todo formatters


def todo_desc_formatter(desc: str, todo: Todo):
    text = desc

    if ts := todo.todos:
        text += f" ({len(ts)})"

    if r := todo.recurrence:
        text += f" !{r.days}d"

    return text


def todo_status_formatter(status: str, todo: Todo):
    if status == "completed":
        return "x"

    if status == "overdue":
        return "!"

    return "o"


def todo_due_formatter(due, _):
    if not due or due == "none":
        return ""

    text = due.strftime("%Y-%m-%d")

    if due.hour:
        text += f" ({due.strftime('%H:%M')})"

    return text


def todo_urgency_formatter(urgency, _, api: DooitAPI):
    theme = api.app.current_theme
    colors = {
        1: theme.green,
        2: theme.yellow,
        3: theme.orange,
        4: theme.red,
    }

    return Text(
        f"!{urgency}",
        style="bold " + colors.get(urgency, theme.primary),
    )


# Workspace formatters


def workspace_desc_formatter(desc: str, workspace: Workspace):
    text = desc

    if ws := workspace.workspaces:
        text += f" ({len(ws)})"

    return text


@subscribe(Startup)
def add_default_themes(api: DooitAPI, _):
    from dooit.api.themes import all_themes

    for theme in all_themes:
        api.css.add_theme(theme)


@subscribe(Startup)
def key_setup(api: DooitAPI, _):
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
    api.keys.set_normal("c", api.toggle_complete)
    api.keys.set_normal("/", api.start_search)
    api.keys.set_normal("ctrl+s", api.start_sort)


@subscribe(Startup)
def layout_setup(api: DooitAPI, _):
    api.layouts.workspace_layout = [WorkspaceWidget.description]
    api.layouts.todo_layout = [
        TodoWidget.status,
        TodoWidget.description,
        TodoWidget.due,
        TodoWidget.urgency,
    ]


@subscribe(Startup)
def formatter_setup(api: DooitAPI, _):
    api.formatter.workspaces.description.add(workspace_desc_formatter)

    api.formatter.todos.status.add(todo_status_formatter)
    api.formatter.todos.description.add(todo_desc_formatter)
    api.formatter.todos.due.add(todo_due_formatter)
    api.formatter.todos.urgency.add(
        partial(todo_urgency_formatter, api=api),
    )


@subscribe(Startup)
def bar_setup(api: DooitAPI, _):
    bar_widgets = [
        StatusBarWidget(get_mode),
        StatusBarWidget(lambda: "", width=0),
        StatusBarWidget(get_clock),
        StatusBarWidget(lambda: " ", width=1),
        StatusBarWidget(get_user),
    ]
    api.bar.set(bar_widgets)


@subscribe(Startup)
def dashboard_setup(api: DooitAPI, _):
    api.dashboard.set(
        [
            "Welcome to Dooit!",
            "",
            "If you're stuck, press '?' for help.",
        ]
    )
