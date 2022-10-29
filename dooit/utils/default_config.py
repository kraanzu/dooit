from dooit.utils.status_widget import Widget
from datetime import datetime

# NOTE: See rich style documentation for details

#################################
#            GENERAL            #
#################################
theme = {}

colors = theme


#################################
#             UTILS             #
#################################
def colored(text: str, color: str, pre: str = ""):
    return f"{pre} [{color}]{text}[/{color}]"


def get_clock() -> str:
    return f"{datetime.now().time().strftime(' {0}  %X ')}".format("C")


def get_date() -> str:
    return f"X {datetime.today().strftime('%d/%m/%Y')}"


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

navbar = {
    "about": {
        "dim": colored("{desc}", "d grey50", " "),
        "highlight": colored("{desc}", "b white", "➜"),
        "edit": colored("{desc}", "b cyan", "➜"),
    },
    "icons": {  # Special icons for specific Workspaces
        "Welcome": "W",
    },
}

EMPTY_NAVBAR = [
    "No workspaces yet?",
    f"Press {colored('a', 'cyan')} to add some!",
]

#################################
#            TODOS              #
#################################

# Column vars:
# desc: description
# due: due date
# urgency: urgency
# eta: estimated time

todo_columns = {
    "desc": 70,
    "due": 20,
    "urgency": 10,
}

# Vars:
# desc: description of the Todo
# icon: icon to show for status
# tags: show tags, if any( modify tag format in extra_fmt )
# recur: show recurrence, if any ( modify tag format in extra_fmt )
todos = {
    "status": {
        "done": "X",
        "pending": "o",
        "overdue": "O",
    },
    "urgency": {
        1: "🅓",
        2: "🅒",
        3: "🅑",
        4: "🅐",
    },
    "extra_fmt": {
        "tag": "T {tags}",  # how to show tags
        "recur": "R {recur}",  # how to show recurrence,
    },
    "about": {
        "dim": colored("{desc}", "d grey50", " "),
        "highlight": colored("{desc}", "b white", "➜"),
        "edit": colored("{desc}", "b cyan", "➜"),
    },
    "due": {
        "dim": colored("{due}", "d grey50"),
        "highlight": colored("{due}", "b white"),
        "edit": colored("{due}", "b cyan"),
    },
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
        func=lambda: " {status} ",
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
        func=get_date,
    ),
]

#################################
#          KEYBINDING           #
#################################
special_keys = {
    "switch pane": "ctrl+i",
    "canel writing": "escape",
    "sort menu toggle": "s",
    "search": ["/", "ctrl+s", "S"],
    "quit": "ctrl+q",
}
