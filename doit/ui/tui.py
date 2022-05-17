from textual.app import App
from textual import events
from textual.widgets import ScrollView
from collections import defaultdict

from doit.ui.widgets import Navbar, Box
from doit.ui.widgets import (
    Entry,
    TodoList,
    HorizontalLine,
    VerticalLine,
    Connector1,
    Connector2,
    Connector3,
    Connector4,
)


class Doit(App):
    def setup_grid(self):
        self.grid.add_row("a", fraction=13)
        self.grid.add_row("sep0", fraction=1)
        self.grid.add_row("b", fraction=80)
        self.grid.add_row("sep1", fraction=1)
        self.grid.add_row("bar", fraction=5)  # A bar at the bottom for looooks :)

        self.grid.add_column("sep0", fraction=1)  # seperator lines
        self.grid.add_column("0", fraction=15)
        self.grid.add_column("sep1", fraction=1)
        self.grid.add_column("sep2", fraction=1)
        self.grid.add_column("1", fraction=53)
        self.grid.add_column("sep3", fraction=1)
        self.grid.add_column("sep4", fraction=1)
        self.grid.add_column("2", fraction=15)
        self.grid.add_column("sep5", fraction=1)
        self.grid.add_column("sep6", fraction=1)
        self.grid.add_column("3", fraction=9)
        self.grid.add_column("sep7", fraction=1)

    def setup_headings(self):
        self.navbar_heading = Box("Menu")
        self.todos_heading = Box("Todo")
        self.due_date_heading = Box("Due Date")
        self.urgency_heading = Box("Urgency")
        placements = {
            "0a": self.navbar_heading,
            "1a": self.todos_heading,
            "2a": self.due_date_heading,
            "3a": self.urgency_heading,
        }

        self.grid.place(**placements)

    def setup_widget_spaces(self):
        middle_areas = dict()
        for i in "0123":
            for j in "ab":
                middle_areas[f"{i}{j}"] = f"{i},{j}"

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
                self.make_box(
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
            )

        self.navbar_box, self.todos_box, self.due_date_box, self.urgency_box = borders

    def make_box(self, areas):
        box = [
            VerticalLine(),
            Connector1(),
            HorizontalLine(),
            Connector2(),
            VerticalLine(),
            Connector4(),
            HorizontalLine(),
            Connector3(),
        ]

        for area, widget in zip(areas, box):
            self.grid.place(**{area: widget})

        return box

    async def on_mount(self):

        # ------- GRID PLACEMENT -------------
        self.grid = await self.view.dock_grid(z=1)
        self.setup_grid()
        self.setup_widget_spaces()
        self.setup_headings()

        self.setup_widget_borders()

        # --------- Widget Init -----------
        self.todo_lists = defaultdict(TodoList)
        self.navbar = Navbar()
        for i in range(10):
            await self.navbar.root.add("All", Entry())

        for i in range(4):
            await self.navbar.root.children[0].add(str(i), Entry())

        placements = {
            "0b": ScrollView(self.navbar, ),
            "1b": self.todo_lists[""],
        }
        self.grid.place(**placements)

        # --------- Widget Placements ----------
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
            case "due_date":
                self.current_tab = self.due_date_heading

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
            await self.todo_lists[""].handle_keypress(event)

        self.refresh()
