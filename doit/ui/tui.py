from textual.app import App
from textual import events
from textual.widget import Widget
from textual.widgets import Static, ScrollView
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
    def setup_table(self):
        self.grid.add_row("a", fraction=13)
        self.grid.add_row("sep0", fraction=1)
        self.grid.add_row("b", fraction=80)
        self.grid.add_row("sep1", fraction=1)
        self.grid.add_row("bar", fraction=5)  # A bar at the bottom for looooks :)

        self.grid.add_column("sep0", fraction=1)  # seperator lines
        self.grid.add_column("1", fraction=15)
        self.grid.add_column("sep1", fraction=1)
        self.grid.add_column("sep2", fraction=1)
        self.grid.add_column("2", fraction=53)
        self.grid.add_column("sep3", fraction=1)
        self.grid.add_column("sep4", fraction=1)
        self.grid.add_column("3", fraction=15)
        self.grid.add_column("sep5", fraction=1)
        self.grid.add_column("sep6", fraction=1)
        self.grid.add_column("4", fraction=9)
        self.grid.add_column("sep7", fraction=1)

    def setup_headings(self):
        self.navbar_box = Box("Menu")
        self.todos_box = Box("Todo")
        self.due_date_box = Box("Due Date")
        self.urgency_box = Box("Urgency")
        placements = {
            "1a": self.navbar_box,
            "2a": self.todos_box,
            "3a": self.due_date_box,
            "4a": self.urgency_box,
        }

        self.grid.place(**placements)

    def setup_widget_spaces(self):
        middle_areas = dict()
        for i in "1234":
            for j in "ab":
                middle_areas[f"{i}{j}"] = f"{i},{j}"

        self.grid.add_areas(**middle_areas)

    async def on_mount(self):

        # ------- GRID PLACEMENT -------------
        self.grid = await self.view.dock_grid(z=1)
        self.setup_table()
        self.setup_headings()
        self.setup_widget_spaces()

        # MIDDLE SEPERATORS
        middle_areas = {f"middle{i}": f"sep{i},b" for i in range(8)}
        self.grid.add_areas(**middle_areas)
        placements = {i: VerticalLine() for i in middle_areas.keys()}
        self.grid.place(**placements)

        # TOP SEPERATORS
        top_areas = {f"top{i}": f"{i},sep0" for i in range(1, 5)}
        self.grid.add_areas(**top_areas)
        placements = {i: HorizontalLine() for i in top_areas.keys()}
        self.grid.place(**placements)

        # BOTTOM SEPERATORS
        bottom_areas = {f"bottom{i}": f"{i},sep1" for i in range(1, 5)}
        self.grid.add_areas(**bottom_areas)
        placements = {i: HorizontalLine() for i in bottom_areas.keys()}
        self.grid.place(**placements)

        # --------- Widget Init -----------
        self.todo_lists = defaultdict(TodoList)
        self.navbar = Navbar()
        for i in range(10):
            await self.navbar.root.add("All", Entry())

        for i in range(4):
            await self.navbar.root.children[0].add(str(i), Entry())

        placements = {
            "1b": ScrollView(self.navbar, gutter=(-1, 0)),
            "2b": self.todo_lists[""],
        }
        self.grid.place(**placements)

        # --------- Widget Placements ----------
        self.navbar_box.highlight()
        self.current_tab = self.navbar_box

    def change_current_tab(self, new_tab: str) -> None:
        """
        Changes the current tab
        """

        self.current_tab.lowlight()
        match new_tab:
            case "navbar":
                self.current_tab = self.navbar_box
            case "todos":
                self.current_tab = self.todos_box
            case "due_date":
                self.current_tab = self.due_date_box

        self.current_tab.highlight()

    async def on_key(self, event: events.Key):
        if event.key == "ctrl+i":
            if self.current_tab == self.navbar_box:
                self.change_current_tab("todos")
            else:
                self.change_current_tab("navbar")
            return

        if self.current_tab == self.navbar_box:
            await self.navbar.handle_keypress(event)
        elif self.current_tab == self.todos_box:
            await self.todo_lists[""].handle_keypress(event)

        self.refresh()
