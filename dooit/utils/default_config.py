from dooit.utils.status_widget import Widget
from datetime import datetime

# NOTE: See rich style documentation for details

#################################
#             UTILS             #
#################################
def colored(text: str, color: str):
    return f"[{color}]{text}[/{color}]"


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
dashboard = [
    ART,
    " \n",
    " \n",
    " \n",
    "Dooit Version 1.0"
]


#################################
#            NAVBAR             #
#################################
# Vars:
# desc: description of the workspace
# icon: icon to show for workspace

navbar = {
    "about": {
        "highlight": " [b white]{desc}[/b white]",
        "dim": " [d grey50]{desc}[/d grey50]",
        "edit": " [b cyan]{desc}[/b cyan]",
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
        "highlight": "[b white]{desc}[/b white]",
        "dim": "[d grey50]{desc}[/d grey50]",
        "edit": "[b cyan]{desc}[/b cyan]",
    },
    "date": {
        "highlight": "[b white]{date}[/b white]",
        "dim": "[d grey50]{date}[/d grey50]",
        "edit": "[b cyan]{date}[/b cyan]",
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
