from typing import Dict, List
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Static
from rich.align import Align
from rich.console import Group, RenderableType
from rich.style import StyleType
from rich.table import Table
from rich.text import Text
from textual import events
from dooit.utils import KeyBinder


# UTILS
# ---------------------------------------------------
NL = Text("\n")
kb = KeyBinder()


def colored(text: str, color: StyleType) -> str:
    return f"[{color}]{text}[/]"


def convert_to_row(bindings: Dict):
    arr = []
    methods = kb.raw

    for i, j in bindings.items():
        if i in methods:
            key = methods[i]
            if isinstance(key, list):
                key = "/".join(key)

            arr.append(
                [
                    Text.from_markup(
                        colored(
                            " or ",
                            "i cyan",
                        ).join(methods[i]),
                        style="b green",
                    ),
                    Text(i, style="magenta"),
                    Text.from_markup(j, style="b blue"),
                ]
            )
        else:
            arr.append(
                [
                    Text(i, style="b green"),
                    Text("N/A", style="d white", justify="center"),
                    Text.from_markup(j, style="b blue"),
                ]
            )

    return arr


def generate_kb_table(
    kb: dict[str, str], topic: str, notes: list[str] = []
) -> RenderableType:
    """
    Generate Table for modes
    """

    arr = convert_to_row(kb)

    table = Table.grid(expand=True, padding=(0, 3))
    table.add_column("mode", width=20)
    table.add_column("keybind", width=15)
    table.add_column("cmd", width=20)
    table.add_column("colon", width=2)
    table.add_column("help", width=50)

    table.add_row(Text.from_markup(f" [r green] {topic} [/r green]"), "", "", "")

    for i in arr:
        table.add_row("", i[0], i[1], Text("->", style="d white"), i[2])

    if notes:
        notes = [f"{colored('!', 'd yellow')} {i}" for i in notes]
        notes = [colored(" Note:", "d white")] + notes

    return Align.center(
        Group(table, *[Text.from_markup(i) for i in notes], NL, seperator, NL)
    )


seperator = Text.from_markup(f"{colored('─' * 60, 'b d black')}", justify="center")

# ---------------- X -------------------------


# KEYBINDINGS
# --------------------------------------------
NORMAL_KB = {
    "move down": "Move down in list",
    "shift down": "Shift todo down in list",
    "move up": "Move up in list",
    "shift up": "Shift todo up in list",
    "toggle complete": "Toggle todo status as complete/incomplete**",
    "copy text": "Copy todo's text",
    "move to top": "Move to top of list",
    "move to bottom": "Move to bottom of list",
    "toggle expand": "Toggle-expand highlighted item",
    "toggle expand parent": "Toggle-expand parent item",
    "remove item": "Remove highlighted node",
    "add sibling": "Add sibling todo/workspace",
    "add child": "Add child todo/workspace",
    "sort menu toggle": "Launch sort menu",
    "start search": "Start Search Mode",
    "switch pane": "Change focused pane",
    "edit due": "Edit date**",
    "edit description": "Edit description**",
    "edit effort": "Edit effort for todo**",
    "edit recurrence": "Edit recurrence for todo**",
    "edit tags": "Edit tags for todo**",
    "increase urgency": "Increase urgency**",
    "decrease urgency": "Decrease urgency**",
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
    "start search": "Go back to search input [i u]if navigating[/i u]",
    "any": "Press key to search input",
}

SORT_KB = {
    "move down": "Move to next sort option",
    "move up": "Move to previous sort option",
    "sort menu toggle": "Cancel sort operation",
    "enter": "Select the sorting method",
}
# ---------------- X -------------------------


# TEXT CONSTS
# --------------------------------------------
HEADER = f"""
{colored("Welcome to the help menu!", 'yellow')}
{seperator.markup}
"""

BODY = f""" {colored(f'Dooit is built to be used from the keyboard!', 'green')}

Documentation below will walk you through the controls:
{seperator.markup}
"""

THANKS = f"{colored('Thanks for using dooit :heart:', 'yellow')}"
AUTHOR = f"{colored('--kraanzu', 'orchid')}{NL.plain * 2}{seperator.markup}{NL}"

OUTRO = (
    f"Press {colored('escape', 'green')} or {colored('?', 'green')} to exit help menu"
)

# ---------------- X -------------------------


class HelpMenu:
    """
    A Help Menu Widget
    """

    header = Text.from_markup(HEADER, justify="center")
    body = Text.from_markup(BODY, justify="center")
    thanks = Text.from_markup(THANKS, justify="center")
    author = Text.from_markup(AUTHOR, justify="center")
    outro = Text.from_markup(OUTRO, justify="center")

    def items(self) -> List[RenderableType]:
        arr = []
        arr.append(self.header)
        arr.append(self.body)
        arr.append(generate_kb_table(NORMAL_KB, "NORMAL", NORMAL_NB))
        arr.append(generate_kb_table(INSERT_KB, "INSERT"))
        arr.append(generate_kb_table(DATE_KB, "DATE", DATE_NB))
        arr.append(generate_kb_table(SEARCH_KB, "SEARCH"))
        arr.append(generate_kb_table(SORT_KB, "SORT"))
        arr.append(self.thanks)
        arr.append(self.author)
        arr.append(self.outro)

        return arr


class HelpScreen(Screen):
    """
    Help Screen to view Help Menu
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "Pop screen"),
        ("question_mark", "app.pop_screen", "Pop screen"),
    ]
    view = Vertical(*[Static(i) for i in HelpMenu().items()])

    def compose(self):
        yield self.view

    async def on_key(self, event: events.Key):
        key = event.character
        if key in ["j", "down"]:
            self.view.scroll_down()
        elif key in ["k", "up"]:
            self.view.scroll_up()
        elif key in ["home", "g"]:
            self.view.scroll_home()
        elif key in ["end", "G"]:
            self.view.scroll_end()
