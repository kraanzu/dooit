from collections import defaultdict
from textual import events
from textual.app import App
from textual.layouts.dock import DockLayout
from textual_extras.events.events import ListItemSelected

from doit.ui.widgets.minimal_scrollview import MinimalScrollView

from doit.ui.events.events import (
    ApplySortMethod,
    HighlightNode,
    ModifyTopic,
    SortNodes,
    UpdateDate,
)
from doit.ui.widgets.search_tree import SearchTree
from doit.ui.widgets.sort_options import SortOptions


from .events import ChangeStatus, Statusmessage, ModifyDue
from ..ui.widgets import (
    Navbar,
    StatusBar,
    Box,
    TodoList,
    HorizontalLine,
    VerticalLine,
    Connector1,
    Connector2,
    Connector3,
    Connector4,
)


class Doit(App):
    async def on_mount(self):
        self.current_menu = ""
        await self.init_vars()
        await self.reset_screen()

    async def init_vars(self):
        self.navbar_heading = Box("Menu")
        self.todos_heading = Box("Todos")

        self.navbar = Navbar()
        self.navbar_scroll = MinimalScrollView(self.navbar)
        self.todo_lists = defaultdict(TodoList)
        self.todo_scroll = dict()
        self.status_bar = StatusBar()

        self.search_tree = SearchTree()

        self.sort_menu = SortOptions(options=["name", "date", "urgency", "status"])
        self.sort_menu.visible = False

        self.current_status = "NORMAL"
        self.navbar_heading.highlight()
        self.current_tab = self.navbar_heading

    async def reset_screen(self):
        await self._clear_screen()
        await self.setup_grid()
        self.setup_widgets()
        await self.refresh_screen()

    async def _clear_screen(self) -> None:
        # clears all the widgets from the screen..and re render them all
        # Why? you ask? this was the only way at the time of this writing

        if isinstance(self.view.layout, DockLayout):
            self.view.layout.docks.clear()
        self.view.widgets.clear()

    async def setup_grid(self):
        self.grid = await self.view.dock_grid()
        self.grid.add_row("a", size=3)
        self.grid.add_row("sep0", fraction=1)
        self.grid.add_row("b", fraction=95)
        self.grid.add_row("sep1", fraction=1)
        self.grid.add_row("bar", fraction=3)  # A bar at the bottom for looooks :)

        self.grid.add_column("sep0", fraction=1)  # seperator lines
        self.grid.add_column("0", fraction=20)
        self.grid.add_column("sep1", fraction=1)
        self.grid.add_column("sep2", fraction=1)
        self.grid.add_column("1", fraction=77)
        self.grid.add_column("sep3", fraction=1)

        self.menu_grid = await self.view.dock_grid(z=1)
        self.menu_grid.add_column("_1", fraction=30)
        self.menu_grid.add_column("mid", fraction=40)
        self.menu_grid.add_column("_2", fraction=30)

        self.menu_grid.add_row("_1", fraction=30)
        self.menu_grid.add_row("mid", fraction=40)
        self.menu_grid.add_row("_2", fraction=30)

        self.menu_grid.add_areas(menu="mid,mid")
        self.menu_grid.place(menu=self.sort_menu)
        # self.sort_menu.vi

    async def toggle_sort_option(self):
        self.sort_menu.visible = not self.sort_menu.visible

    def setup_widgets(self):

        areas = {"nav": "0,a", "todo": "1,a"}

        self.grid.add_areas(**areas)
        placements = {
            "nav": self.navbar_heading,
            "todo": self.todos_heading,
        }

        self.grid.place(**placements)

        # WIDGET SPACES
        middle_areas = dict()
        middle_areas["0b"] = "0,b"
        middle_areas["1b"] = "1,b"

        self.grid.add_areas(**middle_areas)

        # WIDGET BORDERS

        # MIDDLE SEPERATORS
        middle_areas = {f"middle{i}": f"sep{i},b" for i in range(4)}
        self.grid.add_areas(**middle_areas)

        # TOP SEPERATORS
        top_areas = {f"top{i}": f"{i},sep0" for i in range(2)}
        self.grid.add_areas(**top_areas)

        # BOTTOM SEPERATORS
        bottom_areas = {f"bottom{i}": f"{i},sep1" for i in range(2)}
        self.grid.add_areas(**bottom_areas)

        # TOP CONNECTORS
        top_connector_areas = {f"top_connector{i}": f"sep{i},sep0" for i in range(4)}
        self.grid.add_areas(**top_connector_areas)

        # BOTTOM CONNECTORS
        bottom_connector_areas = {
            f"bottom_connector{i}": f"sep{i},sep1" for i in range(4)
        }
        self.grid.add_areas(**bottom_connector_areas)

        borders = []
        for i in range(2):
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

        self.navbar_box = self.make_box(borders[0])
        self.todos_box = self.make_box(borders[1])

    def make_box(
        self,
        areas,
    ):
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

    async def on_resize(self, event: events.Resize) -> None:
        await self.refresh_screen()
        return await super().on_resize(event)

    async def refresh_screen(self):

        self.todo_list = self.todo_lists[self.current_menu]
        if self.current_menu not in self.todo_scroll:
            self.todo_scroll[self.current_menu] = MinimalScrollView(self.todo_list)

        if self.current_status == "SEARCH":
            main_area_widget = self.search_tree
        else:
            main_area_widget = self.todo_scroll[self.current_menu]

        placements = {"0b": (self.navbar_scroll), "1b": main_area_widget}
        self.grid.place(**placements)

        self.grid.add_areas(**{"bar": "0-start|1-end,bar"})
        self.grid.place(bar=self.status_bar)

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

        self.status_bar.clear_message()

        if event.key == "ctrl+i":
            if self.current_tab == self.navbar_heading:
                self.change_current_tab("todos")
            else:
                self.change_current_tab("navbar")
            return

        if self.current_tab == self.navbar_heading:
            await self.navbar.key_press(event)
        else:
            match self.current_status:
                case "SEARCH":
                    await self.search_tree.key_press(event)
                    self.status_bar.set_message(self.search_tree.search.value)
                    self.refresh()

                case "NORMAL":
                    if event.key == "/":
                        await self.search_tree.set_values(self.todo_list.nodes)
                        await self.handle_change_status(
                            ChangeStatus(self, "SEARCH"),
                        )
                        await self.reset_screen()

                    if event.key == "s":
                        await self.toggle_sort_option()
                        return

                    if self.sort_menu.visible:
                        await self.sort_menu.key_press(event)
                        return

                    await self.todo_list.key_press(event)

                case _:
                    await self.todo_list.key_press(event)

        self.refresh()

    # HANDLING EVENTS
    async def handle_change_status(self, event: ChangeStatus):
        status = event.status
        self.current_status = status
        self.status_bar.set_status(status)
        await self.reset_screen()

    # Ik this naming is bad but idk `StatusMessage` was not working :(
    async def handle_statusmessage(self, event: Statusmessage):
        self.status_bar.set_message(event.message)

    async def on_list_item_selected(self, event: ListItemSelected):
        self.current_menu = event.selected
        await self.reset_screen()

    async def handle_modify_due(self, event: ModifyDue):
        await self.todo_list.modify_due_status(event)

    async def handle_modify_topic(self, event: ModifyTopic):
        self.todo_lists[event.new] = self.todo_lists[event.old]
        del self.todo_lists[event.old]

    async def handle_update_date(self, event: UpdateDate):
        self.todo_list.update_date(event.date)

    async def handle_sort_nodes(self, event: SortNodes):
        await self.todo_list._sort_by_arrangement(event.arrangement)

    async def handle_apply_sort_method(self, event: ApplySortMethod):
        await self.todo_list.sort_by(event.method)
        self.sort_menu.visible = False

    async def handle_highlight_node(self, event: HighlightNode):
        await self.todo_list.reach_to_node(event.id)
