from rich.text import Text
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from dooit.utils.status_widget import Widget
from datetime import datetime

# NOTE: See rich style documentation for details

#################################
#            GENERAL            #
#################################
BACKGROUND = "#2e3440"

#################################
#             UTILS             #
#################################


def colored(text: str, color: str, pre: str = ""):
    return f"{pre} [{color}]{text}[/]"


def get_clock() -> Text:
    return Text(f"{datetime.now().time().strftime(' %X ')}", "r yellow")


def get_date() -> Text:
    return Text(f"{datetime.today().strftime(' %d/%m/%Y ')}", "r green")


ART = """\
██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗
██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
██║  ██║███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║
██║  ██║██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ \
"""

#################################
#          DASHBOARD            #
#################################
dashboard = [ART, " \n", " \n", " \n", "Dooit Version 1.0"]


#################################
#            NAVBAR             #
#################################
# Vars:
# desc: description of the workspace
# icon: icon to show for workspace


def stylize_nav(workspace: Workspace, highlight: bool, edit: bool):

    if not highlight:
        return colored("{desc}", "d grey50", " ")
    else:
        if edit:
            colored("{desc}", "b cyan", "➜")
        else:
            return colored("{desc}", "b white", "➜")


nav_item_style = stylize_nav
navbar = {
    "desc": {
        "dim": colored("{desc}", "d grey50", " "),
        "highlight": colored("{desc}", "b white", "➜"),
        "edit": colored("{desc}", "b cyan", "➜"),
    },
}

EMPTY_NAVBAR = [
    "No workspaces yet?",
    f"Press {colored('a', 'cyan')} to add some!",
]

#################################
#            TODOS              #
#################################


# Vars: ( these are the vars which are edited in real time like an input box )
# desc: description of the Todo
# tags: show tags, if any( modify tag format in extra_fmt )
# recur: show recurrence, if any ( modify tag format in extra_fmt )
# eta: estimated time to complete
# urgency: urgency ( 1 - 4 )


def col1(todo: Todo, highlight: bool, edit: bool):
    status = colored("✓", "b green")
    if todo.status == "OVERDUE":
        status = colored("!", "b red")
    elif todo.status == "PENDING":
        status = colored("", "b yellow")

    if not highlight:
        return colored(status + " {eta} {desc} {tags} {recur}", "d grey50", " ")
    else:
        if edit:
            return colored(status + " {eta} {desc} {tags} {recur}", "b cyan", "➜")
        else:
            return colored(status + " {eta} {desc} {tags} {recur}", "b white", "➜")


def col2(todo: Todo, highlight: bool, edit: bool):
    if not highlight:
        return colored("{due}", "d grey50")
    else:
        if edit:
            return colored("{due}", "b white")
        else:
            return colored("{due}", "b cyan")


def col3(todo: Todo, highlight: bool, edit: bool):
    if not highlight:
        return colored("{urgency}", "d grey50")
    else:
        if edit:
            return colored("{urgency}", "b white")
        else:
            return colored("{urgency}", "b cyan")


# A column dict (key, value) => (name -> (ratio, function)) of the columns
# see todos var for rendering
todo_columns = {
    "desc": (80, col1),
    "due": (15, col2),
    "urgency": (5, col3),
}


EMPTY_TODO = [
    "Wow so Empty!?",
    f"Press {colored('a', 'cyan')} to add some!",
]

#################################
#          STATUS BAR           #
#################################
bar = [
    Widget(
        func=lambda: Text("{status}", "r blue"),
    ),
    Widget(
        func=lambda: " {message} ",
        justify="left",
        expand=True,
    ),
    Widget(
        func=get_clock,
    ),
    Widget(
        func=lambda: " ",  # padding
    ),
    Widget(
        func=get_date,
    ),
]

#################################
#          KEYBINDING           #
#################################
special_keys = {
    "switch pane": "tab",
    "canel writing": "escape",
    "sort menu toggle": "s",
    "search": ["/", "ctrl+s", "S"],
    "quit": "ctrl+q",
    "edit tag": "t",
    "edit recurrence": "r",
    "edit eta": "e",
}
