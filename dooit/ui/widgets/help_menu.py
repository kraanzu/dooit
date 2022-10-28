from rich.align import Align
from rich.box import MINIMAL
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.style import StyleType
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from textual.widget import Widget

NL = "\n"


# UTILS
# ---------------------------------------------------


def colored(text: str, color: StyleType) -> str:
    return f"[{color}]{text}[/{color}]"


def generate_kb_table(
    kb: dict[str, str], topic: str, notes: list[str] = []
) -> RenderableType:
    table = Table.grid(expand=False, padding=(0, 0))
    table.add_column("mode")
    table.add_column("cmd")
    table.add_column("colon")
    table.add_column("help")

    table.add_row(Text.from_markup(f" [r green] {topic} [/r green]"), "", "", "")
    for cmd, help in kb.items():
        table.add_row(
            "",
            (Text.from_markup(colored(cmd, "blue"))),
            "",
            (Text.from_markup(colored("  " + help, "magenta")) + NL),
        )

    if notes:
        notes = [f"{colored('', 'd yellow')} {i}" for i in notes]
        notes = [colored(" Note:", "d white")] + notes

    return Align.center(
        Group(table, *[Text.from_markup(i) for i in notes], NL + seperator + NL)
    )


seperator = f"{colored('─' * 60, 'bold dim black')}"

# ---------------- X -------------------------


# KEYBINDINGS
# --------------------------------------------
NORMAL_KB = {
    "j, down": "Move down in list",
    "J, shift+down": "Shift todo down in list",
    "k, up": "Move up in list",
    "K, shift+up": "Shift todo up in list",
    "i": "Edit todo/topic",
    "c": "Toggle todo status as complete/incomplete**",
    "y": "Copy todo's text",
    "d": "Edit date**",
    "+, =": "Increase urgency**",
    "_, -": "Decrease urgency**",
    "g, home": "Move to top of list",
    "G, end": "Move to bottom of list",
    "z": "Toggle-expand highlighted item",
    "Z": "Toggle-expand parent item",
    "x": "Remove highlighted node",
    "a": "Add sibling todo/workspace",
    "A": "Add child todo/workspace",
    "s": "Launch sort menu",
    "/": "Start Search Mode ⃰ ⃰ ",
    "ctrl+i": "Change focused pane",
    "ctrl+q": "Quit the Application",
}

NORMAL_NB = [
    f"{colored('*  - In Menu Only', 'grey50')}",
    f"{colored('** - In Todo List Only', 'grey50')}",
]

INSERT_KB = {
    "escape": "Go back to NORMAL mode",
    "enter": "Continue adding more todos",
    "any": "Push key in the selected item",
}

DATE_KB = {
    "escape": "Go back to normal mode",
    "any": "Enter the key in the focused area",
}

DATE_NB = [
    f"{colored('Only digits and hyphen allowed format:', 'grey50')} {(colored('dd-mm-yyyy', 'yellow'))}"
]

SEARCH_KB = {
    "escape": "Navigate in the searched items"
    + "\n"
    + "Goes back to normal mode [i u]if navigating[/i u]",
    "/": "Go back to search input [i u]if navigating[/i u]",
    "any": "Press key to search input",
}

SORT_KB = {
    f"j, down": "Move down",
    f"k, up": "Move up",
    f"enter": "Select the sorting method",
}
# ---------------- X -------------------------


# TEXT CONSTS
# --------------------------------------------
HEADER = f"""
{colored("Welcome to the help menu!", 'yellow')}
{seperator}
"""

BODY = f""" {colored(f'Dooit is build to be used from the keyboard,{NL} but mouse can also be used to navigate', 'green')}

Documentation below will walk you through the controls:
{seperator}
"""

THANKS = f"{colored('Thanks for using dooit :heart:', 'yellow')}"
AUTHOR = f"{colored('--kraanzu', 'orchid')}{NL * 2}{seperator}{NL}"

OUTRO = f"Press {colored('escape', 'green')} to exit help menu"

# ---------------- X -------------------------


class HelpMenu(Widget):
    """
    A Help Menu Widget
    """

    header = Text.from_markup(HEADER, justify="center")
    body = Text.from_markup(BODY, justify="center")
    thanks = Text.from_markup(THANKS, justify="center")
    author = Text.from_markup(AUTHOR, justify="center")
    outro = Text.from_markup(OUTRO, justify="center")

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True

        tree.add(self.header)
        tree.add(self.body)
        tree.add(generate_kb_table(NORMAL_KB, "NORMAL", NORMAL_NB))
        tree.add(generate_kb_table(INSERT_KB, "INSERT"))
        tree.add(generate_kb_table(DATE_KB, "DATE", DATE_NB))
        tree.add(generate_kb_table(SEARCH_KB, "SEARCH"))
        tree.add(generate_kb_table(SORT_KB, "SORT"))
        tree.add(self.thanks)
        tree.add(self.author)
        tree.add(self.outro)

        return Panel(tree, box=MINIMAL)
