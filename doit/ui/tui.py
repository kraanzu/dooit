from textual.app import App
from textual import events
from textual.widgets import Static, ScrollView
from collections import defaultdict

from doit.ui.widgets import Navbar, Box
from doit.ui.widgets.entry import Entry
from doit.ui.widgets.todo_list import TodoList


class Doit(App):
    async def on_mount(self):

        # ------- GRID PLACEMENT -------------
        self.grid = await self.view.dock_grid(z=1)

        self.grid.add_row("a", fraction=10)
        self.grid.add_row("b", fraction=85)
        self.grid.add_row("blank", fraction=5)  # A Gutter at the bottom for looooks :)

        self.grid.add_column("1", fraction=15)
        self.grid.add_column("sep1", fraction=1)  # seperator lines
        self.grid.add_column("2", fraction=58)
        self.grid.add_column("sep2", fraction=1)
        self.grid.add_column("3", fraction=15)
        self.grid.add_column("sep3", fraction=1)
        self.grid.add_column("4", fraction=9)

        areas = dict()
        for i in "1234":
            for j in "ab":
                areas[f"{i}{j}"] = f"{i},{j}"
        self.grid.add_areas(**areas)

        # HEADING PLACEMENTS
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

        # SEPERATORS
        seperator = "┃" * 100
        areas = {f"sep{i}": f"sep{i},b" for i in range(1, 4)}
        self.grid.add_areas(**areas)
        placements = {i: Static(seperator) for i in areas.keys()}
        self.grid.place(**placements)
        self.navbar_box.highlight()
        self.current_tab = self.navbar_box

        # --------- Widget Init -----------
        self.todo_lists = defaultdict(TodoList)
        self.navbar = Navbar()
        for i in range(30):
            await self.navbar.root.add("All", Entry())

        for i in range(4):
            await self.navbar.root.children[0].add(str(i), Entry())

        placements = {"1b": ScrollView(self.navbar), "2b": self.todo_lists[""]}
        self.grid.place(**placements)

        # --------- Widget Placements ----------
        self.grid.place()

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
