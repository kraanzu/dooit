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
    try:
        username = os.getlogin()
    except OSError:
        uid = os.getuid()
        import pwd

        username = pwd.getpwuid(uid).pw_name
    return Text(f" {username} ", "r " + blue)


#################################
#            COLORS             #
#################################
dark_black = "#242831"
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
BAR_BACKGROUND = black
BORDER_DIM = grey
BORDER_LIT = cyan
BORDER_TITLE_DIM = black
BORDER_TITLE_LIT = white
SEARCH_COLOR = red
YANK_COLOR = blue
SAVE_ON_ESCAPE = False

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
DASHBOARD = [ART, NL, SEP, NL, NL, NL, help_message]
no_search_results = ["🔍", colored("No results found!", red)]


#################################
#           WORKSPACE           #
#################################
WORKSPACE = {
    "dim": grey,
    "highlight": white,
    "editing": cyan,
    "pointer": ">",
    "children_hint": "+",  # "[{count}]", # vars: count
}
EMPTY_WORKSPACE = [
    ":(",
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
    "pointer": ">",
    "children_hint": colored(
        " ({done}/{total})", green
    ),  # vars: remaining, done, total
    # "children_hint": "[b magenta]({remaining}!)[/b magenta]",
    "due_icon": "? ",
    "effort_icon": "+",
    "effort_color": yellow,
    "recurrence_icon": "!",
    "recurrence_color": blue,
    "completed_icon": "x",
    "pending_icon": "o",
    "overdue_icon": "!",
    "urgency1_icon": "A",
    "urgency2_icon": "B",
    "urgency3_icon": "C",
    "urgency4_icon": "D",
}

EMPTY_TODO = [
    ":(",
    "Wow so Empty!?",
    "Add some todos to get started!",
]

#################################
#          STATUS BAR           #
#################################
bar = {
    "A": [(get_status, 0.1)],
    "C": [(get_clock, 1), (get_username)],
}

#################################
#          KEYBINDING           #
#################################
keybindings = {
    "switch pane": "<tab>",
    "sort menu toggle": "<ctrl+s>",
    "start search": ["/", "S"],
    "remove item": "xx",
    "edit effort": "e",
    "edit recurrence": "r",
}
