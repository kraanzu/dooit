from rich.text import Text
from datetime import datetime
import os

# NOTE: See rich style documentation for details

#################################
#             UTILS             #
#################################


def colored(text: str, color: str):
    return f"[{color}]{text}[/]"


def get_status(status):
    return colored(f" {status} ", "r " + blue)


def get_message(message):
    return " " + message


def get_clock() -> Text:
    return Text(f"{datetime.now().time().strftime(' %X ')}", "r " + cyan)


def get_username():
    return Text(f" {os.getlogin()} ", "r " + blue)


#################################
#            COLORS             #
#################################
black = "#2e3440"
white = "#e5e9f0"
grey = "#d8dee9"
red = "#bf616a"
frost_green = "#8fbcbb"
cyan = "#88c0d0"
green = "#a3be8c"
yellow = "#ebcb8b"
blue = "#81a1c1"
magenta = "#b48ead"
orange = "#d08770"


#################################
#            GENERAL            #
#################################
BACKGROUND = black
BORDER_DIM = white
BORDER_LIT = cyan

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

ART = colored(ART, frost_green)
NL = " \n"
SEP = colored("─" * 60, "d " + grey)
help_message = f"Press {colored('?', magenta)} to spawn help menu"
dashboard = [ART, NL, SEP, NL, NL, NL, help_message]


#################################
#           WORKSPACE           #
#################################
WORKSPACE = {
    "dim": grey,
    "highlight": white,
    "editing": cyan,
    "pointer": "> ",
    "children_hint": "",  # "[{count}]", # vars: count
}
EMPTY_WORKSPACE = [
    "🍻",
    "No workspaces yet?",
    f"Press {colored('a', cyan)} to add some!",
]

#################################
#            TODOS              #
#################################


COLUMN_ORDER = ["description", "due", "urgency"]  # order of columns
TODO = {
    "color_todos": False,
    "dim": grey,
    "highlight": white,
    "editing": cyan,
    "pointer": "> ",
    "children_hint": colored(
        " ({done}/{total})", green
    ),  # vars: remaining, done, total
    # "children_hint": "[b magenta]({remaining}!)[/b magenta]",  # vars: remaining, done, total
    "due_icon": "🕑",
    "effort_icon": "🗲 ",
    "effort_color": yellow,
    "recurrence_icon": " ⟲ ",
    "recurrence_color": blue,
    "tags_icon": "🖈 ",
    "tags_seperator": "icon",  # icon, pipe, comma
    "tags_color": red,
    "completed_icon": "✓ ",
    "pending_icon": "● ",
    "overdue_icon": "! ",
    "urgency1_icon": "🅐",
    "urgency2_icon": "🅑",
    "urgency3_icon": "🅒",
    "urgency4_icon": "🅓",
}

EMPTY_TODO = [
    "🤘",
    "Wow so Empty!?",
    "Add some todos to get started!",
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
