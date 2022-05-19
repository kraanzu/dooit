from textual import events
from textual.app import App
from textual.events import Key
from textual.widgets import ScrollView


from ..ui.widgets import (
    Navbar,
    StatusBar,
    Box,
    Empty,
    DateTree,
    UrgencyTree,
    TodoList,
    HorizontalLine,
    VerticalLine,
    Connector1,
    Connector2,
    Connector3,
    Connector4,
)

from .events import Keystroke


class Doit(App):
    def setup_grid(self):
        self.grid.add_row("a", size=3)
        self.grid.add_row("sep0", fraction=1)
        self.grid.add_row("b", fraction=95)
        self.grid.add_row("sep1", fraction=1)
        self.grid.add_row("bar", fraction=3)  # A bar at the bottom for looooks :)

        self.grid.add_column("sep0", fraction=1)  # seperator lines
        self.grid.add_column("0", fraction=15)
        self.grid.add_column("sep1", fraction=1)
        self.grid.add_column("sep2", fraction=1)
        self.grid.add_column("1", fraction=50)
        self.grid.add_column("sep3", fraction=1)
        self.grid.add_column("sep4", fraction=1)
        self.grid.add_column("2", fraction=17)
        self.grid.add_column("sep5", fraction=1)
        self.grid.add_column("sep6", fraction=1)
        self.grid.add_column("3", fraction=10)
        self.grid.add_column("sep7", fraction=1)

    def setup_headings(self):
        self.navbar_heading = Box("Menu")
        self.todos_heading = Box("Todos")

        areas = {"nav": "0,a", "todo": "1-start|3-end,a"}

        self.grid.add_areas(**areas)
        placements = {
            "nav": self.navbar_heading,
            "todo": self.todos_heading,
        }

        self.grid.place(**placements)

    def setup_widget_spaces(self):
        middle_areas = dict()
        for i in "0123":
            middle_areas[f"{i}b"] = f"{i},b"

        self.grid.add_areas(**middle_areas)

    def setup_widget_borders(self):
        # MIDDLE SEPERATORS
        middle_areas = {f"middle{i}": f"sep{i},b" for i in range(8)}
        self.grid.add_areas(**middle_areas)

        # TOP SEPERATORS
        top_areas = {f"top{i}": f"{i},sep0" for i in range(4)}
        self.grid.add_areas(**top_areas)

        # BOTTOM SEPERATORS
        bottom_areas = {f"bottom{i}": f"{i},sep1" for i in range(4)}
        self.grid.add_areas(**bottom_areas)

        # TOP CONNECTORS
        top_connector_areas = {f"top_connector{i}": f"sep{i},sep0" for i in range(8)}
        self.grid.add_areas(**top_connector_areas)

        # BOTTOM CONNECTORS
        bottom_connector_areas = {
            f"bottom_connector{i}": f"sep{i},sep1" for i in range(8)
        }
        self.grid.add_areas(**bottom_connector_areas)

        borders = []
        for i in range(4):
            borders.append(
                [
                    f"middle{2 * i}",
                    f"top_connector{2 * i}",
                    f"top{i}",
                    f"top_connector{2 * i + 1}",
                    f"middle{2 * i + 1}",
                    f"bottom_connector{2 * i + 1}",
                    f"bottom{i}",
                    f"bottom_connector{2 * i}",
                ]
            )

        self.navbar_box = self.make_box(
            borders[0],
        )
        self.todos_box = self.make_box(borders[1], right=False)
        self.due_date_box = self.make_box(borders[2], left=False, right=False)
        self.urgency_box = self.make_box(borders[3], left=False)

    def make_box(
        self,
        areas,
        left: bool = True,
        top: bool = True,
        bottom: bool = True,
        right: bool = True,
    ):
        box = [
            VerticalLine() if left else Empty(),
            Connector1() if left and top else HorizontalLine(),
            HorizontalLine() if top else Empty(),
            Connector2() if top and right else HorizontalLine(),
            VerticalLine() if right else Empty(),
            Connector4() if right and bottom else HorizontalLine(),
            HorizontalLine() if bottom else Empty(),
            Connector3() if bottom and left else HorizontalLine(),
        ]

        for area, widget in zip(areas, box):
            self.grid.place(**{area: widget})

        return box

    async def on_mount(self):
        self.current_menu = ""
        self.grid = await self.view.dock_grid()
        self.setup_grid()
        self.setup_widget_spaces()
        self.setup_headings()

        self.setup_widget_borders()
        await self.setup_screen()

    async def setup_screen(self):
        self.navbar = Navbar()
        self.todo_lists = TodoList()
        self.dates = DateTree()
        self.urgency_trees = UrgencyTree()

        placements = {
            "0b": ScrollView(
                self.navbar,
            ),
            "1b": self.todo_lists,
            "2b": self.dates,
            "3b": self.urgency_trees,
        }
        self.grid.place(**placements)

        self.status_bar = StatusBar()
        self.grid.add_areas(**{"bar": "0-start|3-end,bar"})
        self.grid.place(bar=self.status_bar)

        self.navbar_heading.highlight()
        self.current_tab = self.navbar_heading

    def change_current_tab(self, new_tab: str) -> None:
        """
        Changes the current tab
        """

        self.current_tab.lowlight()
        match new_tab:
            case "navbar":
                self.current_tab = self.navbar_heading
            case "todos":
                self.current_tab = self.todos_heading

        self.current_tab.highlight()

    async def on_key(self, event: events.Key):
        if event.key == "ctrl+i":
            if self.current_tab == self.navbar_heading:
                self.change_current_tab("todos")
            else:
                self.change_current_tab("navbar")
            return

        if self.current_tab == self.navbar_heading:
            await self.navbar.handle_keypress(event)
        elif self.current_tab == self.todos_heading:
            await self.todo_lists.handle_keypress(event)

        self.refresh()

    async def handle_keystroke(self, event: Keystroke):
        await self.dates.handle_keypress(Key(self, event.key))
        await self.urgency_trees.handle_keypress(Key(self, event.key))
