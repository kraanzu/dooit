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


def generate_kb_table(kb: dict[str, str], topic: str) -> RenderableType:
    table = Table.grid(expand=True, padding=(0, -1))
    table.add_column("mode", width=12)
    table.add_column("cmd", width=10)
    table.add_column("colon", width=2)
    table.add_column("help")

    table.add_row(Text.from_markup(f" [r blue] {topic} [/r blue]"), "", "", "")
    for cmd, help in kb.items():
        table.add_row(
            "",
            (Text.from_markup(colored(cmd, "blue"))),
            "",
            (Text.from_markup(colored(" " + help, "magenta")) + NL),
        )

    return Align.center(Group(table, NL + seperator + NL))


seperator = f"{colored('─' * 60, 'bold dim black')}"

# ---------------- X -------------------------


# KEYBINDINGS
# --------------------------------------------
NORMAL_KB = {
    "j/down": "move down",
    "k/up": "move up",
    "i": "edit data",
    "g": "move to top",
    "G": "move to bottom",
    "z": "toggle-expand highlighted node",
    "Z": "toggle-expand parent node",
    "x": "remove highlighted node",
    "a": "add sibling",
    "A": "add child",
}

INSERT_KB = {
    "escape": "Go back to normal mode",
    "any": "Enter the key in the focused area",
}

DATE_KB = {
    "escape": "Go back to normal mode",
    "any": "Enter the key in the focused area"
    + "\n"
    + "Only digits and hyphen allowed",
}

SEARCH_KB = {
    "escape": "Navigate in the searched items"
    + "\n"
    + "Goes back to normal mode [i u]if navigating[/i u]",
    "/": "Go back to search input [i u]if navigating[/i u]",
    "any": "Press key to search input",
}

SORT_KB = {
    "j": "Move down",
    "k": "Move up",
    "enter": "Select the sorting method",
}
# ---------------- X -------------------------


# TEXT CONSTS
# --------------------------------------------
HEADER = f"""
{colored("Welcome to the help menu!", 'yellow')}
{seperator}
"""

BODY = f"""
{colored(f'Doit is build to be used from the keyboard,{NL} but mouse can also be used to navigate', 'green')}

Documentation below will wak you through the controls:
{seperator}
"""

FOOTER = f"{colored('Thanks for using doit :heart:', 'yellow')}"
AUTHOR = f"{colored('--kraanzu', 'orchid')}"

# ---------------- X -------------------------


class HelpMenu(Widget):
    """
    A Help Menu Widget
    """

    header = Text.from_markup(HEADER, justify="center")
    body = Text.from_markup(BODY, justify="center")
    footer = Text.from_markup(FOOTER, justify="center")
    author = Text.from_markup(AUTHOR, justify="center")

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True

        tree.add(self.header)
        tree.add(self.body)
        tree.add(generate_kb_table(NORMAL_KB, "NORMAL"))
        tree.add(generate_kb_table(INSERT_KB, "INSERT"))
        tree.add(generate_kb_table(DATE_KB, "DATE"))
        tree.add(generate_kb_table(SEARCH_KB, "SEARCH"))
        tree.add(generate_kb_table(SORT_KB, "SORT"))
        tree.add(self.footer)
        tree.add(self.author)

        return Panel(tree, box=MINIMAL)
