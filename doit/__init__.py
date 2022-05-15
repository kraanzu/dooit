from rich.align import Align
from rich.panel import Panel
from rich.text import Text, TextType
from textual.app import App
from textual.widgets import Static
from doit.ui.widgets.entry import Entry

from doit.ui.widgets.navbar import Navbar
from doit.ui.widgets.todo_list import TodoList


def percent(percent, total):
    return int(percent * total / 100)


def centered(text: str):
    return Static(
        Panel(
            Align.center(Text(text, style="cyan"), vertical="middle"),
            border_style="dim green",
        ),
    )


def main():
    class ok(App):
        async def on_mount(self):
            g = await self.view.dock_grid(z=1)
            g.add_row("a", fraction=10)
            g.add_row("b", fraction=85)
            g.add_row("blank", fraction=5)

            g.add_column("1", fraction=15)
            g.add_column("sep1", fraction=1)
            g.add_column("2", fraction=58)
            g.add_column("sep2", fraction=1)
            g.add_column("3", fraction=15)
            g.add_column("sep3", fraction=1)
            g.add_column("4", fraction=9)

            areas = dict()
            for i in "1234":
                for j in "ab":
                    areas[f"{i}{j}"] = f"{i},{j}"
            g.add_areas(**areas)

            # HEADING PLACEMENTS
            placements = {
                "1a": "Menu",
                "2a": "Todos",
                "3a": "Due Date",
                "4a": "Urgency",
            }
            placements = {i: centered(j) for i, j in placements.items()}
            g.place(**placements)

            # SEPERATORS
            seperator = "┃" * 100
            areas = {f"sep{i}": f"sep{i},b" for i in range(1, 4)}
            g.add_areas(**areas)
            placements = {i: Static(seperator) for i in areas.keys()}
            g.place(**placements)

            x = TodoList("x")
            for i in range(10):
                await x.root.add("", Entry("hi"))

            placements = {"1b": Navbar(""), "2b": x}
            g.place(**placements)

    ok.run()
