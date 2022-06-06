from textual import events
from textual.app import App
from textual.layouts.dock import DockLayout
from textual.widget import Widget
from textual_extras.events.events import ListItemSelected

from .events import *
from ..ui.widgets import *
from ..utils import Parser

parser = Parser()


class Doit(App):
    async def on_mount(self) -> None:
        self.current_menu = ""
        await self.init_vars()
        await self.reset_screen()

        for widget in self.navbar_box:
            widget.toggle_highlight()

    async def action_quit(self) -> None:
        await super().action_quit()
        parser.save_todo(self.todo_lists_copy)
        parser.save_topic(self.navbar_copy)

    async def init_vars(self) -> None:
        """
        Init class Vars
        """

        self.navbar_heading = Box([" Menu"])
        self.todos_heading = Box([" Todos"])

        self.navbar = parser.parse_topic()
        self.navbar_copy = parser.parse_topic()  # copy for storage

        self.navbar_scroll = MinimalScrollView(self.navbar)
        self.todo_lists = parser.parse_todo()
        self.todo_lists_copy = parser.parse_todo()

        self.todo_scroll = dict()
        self.status_bar = StatusBar()

        self.search_tree = SearchTree()

        self.sort_menu = SortOptions(options=["name", "date", "urgency", "status"])
        # self.sort_menu.visible = False

        self.current_status = "NORMAL"
        self.navbar_heading.highlight()
        self.current_tab = self.navbar_heading

    async def reset_screen(self) -> None:
        """
        Reloads the screen
        """

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

    async def _make_grid(self, grid):
        grid.add_row("a", size=3)
        grid.add_row("sep0", fraction=1)
        grid.add_row("b", fraction=95)
        grid.add_row("sep1", fraction=1)
        grid.add_row("bar", fraction=3)

        grid.add_column("sep0", fraction=1)
        grid.add_column("0", fraction=20)
        grid.add_column("sep1", fraction=1)
        grid.add_column("sep2", fraction=1)
        grid.add_column("1", fraction=77)
        grid.add_column("sep3", fraction=1)

    async def setup_grid(self) -> None:
        """
        Handle grid placing
        """

        self.grid = await self.view.dock_grid()
        await self._make_grid(self.grid)

    def setup_widgets(self) -> None:
        """
        Place widgets
        """

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

        self.navbar_box = self._make_box(borders[0])
        self.todos_box = self._make_box(borders[1])

    def _make_box(self, areas: dict[str, str]) -> list[Widget]:
        """
        Make border for trees
        """

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

    async def refresh_screen(self) -> None:
        """
        Re-place all the widgets
        """

        if self.current_menu not in self.todo_lists.keys():
            self.todo_lists[self.current_menu] = TodoList()
            self.todo_lists_copy[self.current_menu] = TodoList()

        self.todo_list = self.todo_lists[self.current_menu]
        self.todo_list_copy = self.todo_lists_copy[self.current_menu]

        if self.current_menu not in self.todo_scroll:
            self.todo_scroll[self.current_menu] = MinimalScrollView(self.todo_list)

        match self.current_status:
            case "SEARCH":
                main_area_widget = self.search_tree
            case "SORT":
                main_area_widget = self.sort_menu
            case _:
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

        def dim(var):
            for i in var:
                i.dim()

        def illuminate(var):
            for i in var:
                i.illuminate()

        match new_tab:
            case "navbar":
                self.current_tab = self.navbar_heading
                illuminate(self.navbar_box)
                dim(self.todos_box)
            case "todos":
                self.current_tab = self.todos_heading
                dim(self.navbar_box)
                illuminate(self.todos_box)

        self.current_tab.highlight()

    async def show_sort_menu(self):
        await self.handle_change_status(ChangeStatus(self, "SORT"))
        self.sort_menu.visible = True
        self.refresh()

    async def on_key(self, event: events.Key) -> None:

        self.status_bar.clear_message()

        if event.key == "ctrl+i":
            if self.current_tab == self.navbar_heading:
                self.change_current_tab("todos")
            else:
                self.change_current_tab("navbar")
            return

        if self.current_tab == self.navbar_heading:
            await self.navbar.key_press(event)
            await self.navbar_copy.key_press(event)
        else:
            match self.current_status:
                case "SEARCH":
                    await self.search_tree.key_press(event)
                    self.status_bar.set_message(self.search_tree.search.value)
                    self.refresh()

                case "SORT":
                    await self.sort_menu.key_press(event)

                case "NORMAL":
                    if event.key == "/":
                        await self.search_tree.set_values(self.todo_list.nodes)
                        await self.handle_change_status(
                            ChangeStatus(self, "SEARCH"),
                        )
                        await self.reset_screen()

                    elif event.key == "s":
                        await self.handle_change_status(
                            ChangeStatus(self, "SORT"),
                        )

                    else:
                        await self.todo_list.key_press(event)
                        await self.todo_list_copy.key_press(event)

                case _:
                    await self.todo_list.key_press(event)
                    await self.todo_list_copy.key_press(event)

        self.refresh()

    # HANDLING EVENTS
    async def handle_change_status(self, event: ChangeStatus) -> None:
        status = event.status
        reset = (self.current_status in ["SEARCH", "SORT"]) or status == "SORT"
        self.current_status = status
        self.status_bar.set_status(status)

        if reset:
            await self.reset_screen()

        # if status in ["NORMAL"]:
        #     self.change_current_tab(self.current_tab)

    async def handle_notify(self, event: Notify) -> None:
        self.status_bar.set_message(event.message)

    async def on_list_item_selected(self, event: ListItemSelected) -> None:
        self.status_bar.set_message(
            f"{event.selected} | {event.selected in self.todo_lists}"
        )
        self.current_menu = event.selected
        await self.reset_screen()

        self.change_current_tab("todos" if event.focus else "navbar")

    async def handle_modify_topic(self, event: ModifyTopic) -> None:
        self.status_bar.set_message(
            f"{event.old} to {event.new} | {event.old in self.todo_lists}"
        )

        if event.old == event.new:
            return

        if event.old == "/" or event.old.endswith("//"):
            return

        self.todo_lists[event.new] = self.todo_lists.get(event.old, TodoList())
        self.todo_lists_copy[event.new] = self.todo_lists_copy.get(
            event.old, TodoList()
        )

        if event.old in self.todo_lists:
            del self.todo_lists[event.old]
            del self.todo_lists_copy[event.old]

    async def handle_apply_sort_method(self, event: ApplySortMethod) -> None:
        await self.todo_list.sort_by(event.method)

    async def handle_highlight_node(self, event: HighlightNode) -> None:
        await self.todo_list.reach_to_node(event.id)
