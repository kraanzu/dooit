from rich.text import Text
from datetime import datetime
import os

# NOTE: See rich style documentation for details

#################################
#             UTILS             #
#################################


def colored(text: str, color: str, pre: str = ""):
    return f"{pre} [{color}]{text}[/]"


def get_status(status):
    return colored(f" {status} ", "r blue")


def get_message(message):
    return " " + message


def get_clock() -> Text:
    return Text(f"{datetime.now().time().strftime(' %X ')}", "r cyan")


def get_username():
    return Text(f" {os.getlogin()} ", "r blue")


#################################
#            GENERAL            #
#################################
BACKGROUND = "#2e3440"
DATE_ORDER = "DMY"  # can be any permutation of 'D', 'M' and 'Y'
BORDER_DIM = "dim white"
BORDER_LIT = "bold cyan"

#################################
#          DASHBOARD            #
#################################

ART = """
██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗  █████╗ ██████╗ ██████╗
██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗██╔══██╗██╔══██╗
██║  ██║███████║███████╗███████║██████╔╝██║   ██║███████║██████╔╝██║  ██║
██║  ██║██╔══██║╚════██║██╔══██║██╔══██╗██║   ██║██╔══██║██╔══██╗██║  ██║
██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝\
"""

dashboard = [ART, " \n", " \n", " \n", "Dooit Version 1.0"]


#################################
#           WORKSPACE           #
#################################
WORKSPACE = {
    "dim": "d grey50",
    "highlight": "b white",
    "editing": "b cyan",
    "pointer": "> ",
    "children_hint": "",  # "[{count}]", # vars: count
}
EMPTY_WORKSPACE = [
    "No workspaces yet?",
    f"Press {colored('a', 'cyan')} to add some!",
]

#################################
#            TODOS              #
#################################


COLUMN_ORDER = ["description", "due", "urgency"]  # order of columns
TODO = {
    "dim": "d grey50",
    "highlight": "b white",
    "editing": "b cyan",
    "pointer": "> ",
    "children_hint": " [b green]({done}/{total})[/b green]",  # vars: remaining, done, total
    # "children_hint": "[b magenta]({remaining}!)[/b magenta]",  # vars: remaining, done, total
    "due_icon": "🕑",
    "effort_icon": "🗲 ",
    "effort_color": "yellow",
    "recurrence_icon": " ⟲ ",
    "recurrence_color": "blue",
    "tags_icon": "🖈 ",
    "tags_seperator": "icon",  # icon, pipe, comma
    "tags_color": "red",
    "completed_icon": "✓ ",
    "pending_icon": "● ",
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
bar = {
    "A": [get_status],
    "B": [get_message],
    "C": [get_clock, get_username],
}

#################################
#          KEYBINDING           #
#################################
keybindings = {
    "switch pane": "<tab>",
    "sort menu toggle": "<ctrl+s>",
    "start search": ["/", "S"],
    "remove item": "xx",
    "edit tags": "t",
    "edit effort": "e",
    "edit recurrence": "r",
}
