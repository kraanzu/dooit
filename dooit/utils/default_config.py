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

dark_black = "#252a34"
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
WORKSPACES_BACKGROUND = black
TODOS_BACKGROUND = black
BORDER_DIM = grey + " 50%"
BORDER_LIT = blue
BORDER_TITLE_DIM = grey, dark_black
BORDER_TITLE_LIT = white, blue
SEARCH_COLOR = red
YANK_COLOR = blue
SAVE_ON_ESCAPE = False
USE_DAY_FIRST = True
DATE_FORMAT = "%d %h"
TIME_FORMAT = "%H:%M"

#################################
#          DASHBOARD            #
#################################
legend = {"B": blue, "O": orange, "G": green, "M": magenta}
legend = {i + "]": j + "]" for i, j in legend.items()}

regex_style = {
    "U": red,
    "Y": grey,
    "6": blue,
    "a": blue,
    "#": yellow,
    r"(?<=\()[^()\n]+(?=\))": white,
}


def change(s: str):
    for i, j in legend.items():
        s = s.replace(i, j)

    return s


def stylize(art):
    art = "\n".join([change(i) for i in art])
    art = Text.from_markup(art)
    for i, j in regex_style.items():
        art.highlight_regex(i, j)

    return art


art = [
    r"[B]       __I___       [/B][M]                                      [/M]",
    r"[B]   .-''  .  ''-.    [/B][M]                                      [/M]",
    r"[B] .'  / . ' . \  '.  [/B][M]                                      [/M]",
    r"[B]/_.-..-..-..-..-._\ [/B][G] .----------------------------------. [/G]",
    r"[O]         #  _,,_    [/O][G]( Can you complete your tasks today? )[/G]",
    r"[O]         #/`    `\  [/O][G]/'----------------------------------' [/G]",
    r"[O]         / / 6 6\ \ [/O][M]                                      [/M]",
    r"[O]         \/\  Y /\/ [/O][M]       /\_/\                          [/M]",
    r"[O]         #/ `'U` \  [/O][M]      /a a  \               _         [/M]",
    r"[O]       , (  \   | \ [/O][M]     =\ Y  =/-~~~~~~-,_____/ /        [/M]",
    r"[O]       |\|\_/#  \_/ [/O][M]       '^--'          ______/         [/M]",
    r"[O]       \/'.  \  /'\ [/O][M]         \           /                [/M]",
    r"[O]        \    /=\  / [/O][M]         ||  |---'\  \                [/M]",
    r"[O]        /____)/____)[/O][M]        (_(__|   ((__|                [/M]",
]

ART = stylize(art)
NL = " \n"
SEP = colored("─" * 60, "d " + grey)
help_message = f"Press {colored('?', magenta)} to spawn help menu"
DASHBOARD = [ART, NL, SEP, NL, NL, NL, help_message]
no_search_results = ["🔍", colored("No results found!", red)]


#################################
#           WORKSPACE           #
#################################
WORKSPACE = {
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
    "tags_color": red,
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
