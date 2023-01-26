from rich.text import Text
from dooit.utils.status_widget import Widget
from datetime import datetime
import os

# NOTE: See rich style documentation for details

#################################
#            GENERAL            #
#################################
BACKGROUND = "#2e3440"
DATE_ORDER = "DMY"  # can be any permutation of 'D', 'M' and 'Y'
BORDER_DIM = "dim white"
BORDER_LIT = "bold cyan"

#################################
#             UTILS             #
#################################


def colored(text: str, color: str, pre: str = ""):
    return f"{pre} [{color}]{text}[/]"


def get_clock() -> Text:
    return Text(f"{datetime.now().time().strftime(' %X ')}", "r cyan")


def get_username():
    return Text(f" {os.getlogin()} ", "r blue")


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
#           WORKSPACE           #
#################################
WORKSPACE = {
    "dim": "d grey50",
    "highlight": "b white",
    "editing": "b cyan",
    "pointer": "▍",
    "children_hint": "[{count}]",
}
EMPTY_WORKSPACE = [
    "No workspaces yet?",
    f"Press {colored('a', 'cyan')} to add some!",
]

#################################
#            TODOS              #
#################################


COLUMN_ORDER = ["desc", "due", "urgency"]  # order of columns
TODO = {
    "dim": "d grey50",
    "highlight": "b white",
    "editing": "b cyan",
    "pointer": "► ",
    "children_hint": " [{done}/{total}]",  # vars: remaining, done, total
    "due_icon": "🕑",
    "eta_icon": " ⌚",
    "eta_color": "b yellow",
    "recurrence_icon": " ⟲ ",
    "recurrence_color": "b blue",
    "tags_icon": " 🏷 ",
    "tags_seperator": "comma",  # icon, pipe, comma
    "tags_color": "b red",
    "completed_icon": "✓ ",
    "pending_icon": " ",
    "overdue_icon": "! ",
    "urgency1_icon": "🅐",
    "urgency2_icon": "🅑",
    "urgency3_icon": "🅒",
    "urgency4_icon": "🅓",
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
        func=lambda: Text(
            " {status} ",
            "r blue",
        ),
    ),
    Widget(
        func=lambda: " {message} ",
        expand=True,
    ),
    Widget(
        func=get_clock,
    ),
    Widget(
        func=get_username,
    ),
]

#################################
#          KEYBINDING           #
#################################
special_keys = {
    "switch pane": "tab",
    "canel writing": "escape",
    "sort menu toggle": "ctrl+s",
    "search": ["/", "S"],
    "quit": "ctrl+q",
    "edit tag": "t",
    "edit recurrence": "r",
    "edit eta": "e",
}
