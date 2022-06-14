from rich.align import Align
from rich.box import MINIMAL
from rich.console import RenderableType
from rich.panel import Panel
from rich.style import StyleType
from rich.table import Table
from rich.text import Text
from rich.tree import Tree
from textual import events
from textual.widget import Widget

NL = "\n"


# UTILS
# ---------------------------------------------------


def colored(text: str, color: StyleType) -> str:
    return f"[{color}]{text}[/{color}]"


def generate_kb_table(kb: dict[str, str]) -> RenderableType:
    table = Table.grid(
        padding=(-10, 0, -10, 5),
        expand=True,
    )
    table.add_column("cmd", width=6)
    table.add_column("colon", width=1)
    table.add_column("help")

    for cmd, help in kb.items():
        table.add_row(
            (Text.from_markup(colored(cmd, "b blue"))),
            "",
            (Text.from_markup(colored(" " + help, "b magenta")) + NL),
        )

    return Align.center(table)


seperator = f"{colored('─' * 60, 'bold dim black')}"

# ---------------- X -------------------------


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

    async def key_press(self, event: events.Key):
        pass

    def render(self) -> RenderableType:
        tree = Tree("")
        tree.hide_root = True
        tree.expanded = True

        tree.add(self.header)
        tree.add(self.body)
        tree.add(generate_kb_table(NORMAL_KB))
        tree.add(self.footer)
        tree.add(self.author)

        return Panel(tree, box=MINIMAL)
