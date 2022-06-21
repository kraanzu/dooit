from os import get_terminal_size
from rich.align import Align
from rich.console import Group
from rich.text import Text
from dooit.utils.parser import Parser

parser = Parser()
from dooit.utils.config import conf

keys = conf.keys
message = conf.load_config("welcome_message")
ascii_art = conf.load_config("ascii_art")


from textual import events
from textual.app import App
from textual.layouts.dock import DockLayout
from textual.layouts.grid import GridLayout
from textual.widget import Widget


from .events import *  # NOQA
from ..ui.widgets import *  # NOQA

BANNER = Text(
    f"""
    {ascii_art}

""",
    style="green",
)

WELCOME = Text(
    f"""
                   
    {message}
""",
    style="magenta",
)

HELP = Text.from_markup(
    f"""
    Anyways, Press [bold yellow]`{keys.show_help[0]}`[/bold yellow] to show help menu
""",
    style="cyan",
)


class Doit(App):
    async def on_mount(self) -> None:
        self.current_menu = ""
        self.main_area_scroll = MinimalScrollView()
        await self.init_vars()

        await self.setup_screen()

        self.help = False

        for widget in self.navbar_box:
            widget.toggle_highlight()

    async def on_load(self) -> None:
        await self.bind("ctrl+q", "quit", "Quit")

    async def action_quit(self) -> None:
        await self.on_key(events.Key(self, "escape"))  # incase of empty todo
        await super().action_quit()
        parser.save(self.todo_lists)

    async def toggle_help(self):
        self.help = not self.help

        await self._clear_screen()
        if self.help:
            self.help_menu = MinimalScrollView(HelpMenu())
            await self.view.dock(self.help_menu)
        else:
            await self.setup_screen()

    async def setup_screen(self):
        await self.setup_grid()
        self.setup_areas()
        self.place_widgets()
        await self.reset_screen()

    async def _clear_screen(self) -> None:
        """
        Removes all the widgets and clears the window
        """

        if isinstance(self.view.layout, DockLayout):
            self.view.layout.docks.clear()
        self.view.widgets.clear()

    async def init_vars(self) -> None:
        """
        Init class Vars
        """

        self.navbar_heading = Box(name="navbar", options=[" Menu"])
        self.todos_heading = Box(name="todos", options=[" Todos"])

        self.navbar, self.todo_lists = await parser.load()

        self.navbar_scroll = MinimalScrollView(self.navbar)

        self.status_bar = StatusBar()
        self.search_tree = SearchTree()
        self.sort_menu = SortOptions(options=["name", "date", "urgency", "status"])

        self.current_status = "NORMAL"
        self.navbar_heading.highlight()
        self.current_tab = self.navbar_heading

    async def reset_screen(self) -> None:
        """
        Reloads the screen
        """
        await self.refresh_screen()

    async def _make_grid(self, grid: GridLayout) -> None:
        grid.add_row("a", size=3)
        grid.add_row("sep0", size=1)
        grid.add_row("b")
        grid.add_row("sep1", size=1)
        grid.add_row("bar", size=1)

        grid.add_column("sep0", size=1)
        grid.add_column("0", fraction=20)
        grid.add_column("sep1", size=1)
        grid.add_column("padding", size=1)
        grid.add_column("sep2", size=1)
        grid.add_column("1", fraction=80)
        grid.add_column("sep3", size=1)

    async def setup_grid(self) -> None:
        """
        Handle grid placing
        """

        self.grid = await self.view.dock_grid()
        await self._make_grid(self.grid)

    def place_widgets(self):
        placements = {
            "nav": self.navbar_heading,
            "todo": self.todos_heading,
        }

        self.grid.place(**placements)

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

        self.grid.place(bar=self.status_bar)
        self.grid.place(
            **{
                "0b": (self.navbar_scroll),
            }
        )

        placements = {"1b": self.main_area_scroll}
        self.grid.place(**placements)

    def setup_areas(self) -> None:
        """
        Place widgets
        """

        areas = {
            "nav": "sep0-start|sep1-end,a",
            "todo": "sep2-start|sep3-end,a",
        }

        self.grid.add_areas(**areas)

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

        self.grid.add_areas(**{"bar": "0-start|1-end,bar"})

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

        self.todo_list = self.todo_lists[self.current_menu]

        if self.current_menu == "":
            main_area_widget = Align.center(
                Group(BANNER, WELCOME, HELP),
                vertical="middle",
                height=round(get_terminal_size()[1] * 0.8),
            )
        else:
            match self.current_status:
                case "SEARCH":
                    main_area_widget = self.search_tree
                case "SORT":
                    main_area_widget = self.sort_menu
                case _:
                    main_area_widget = self.todo_lists[self.current_menu]

        await self.main_area_scroll.update(main_area_widget)

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

    def switch_tabs(self):
        if self.current_tab == self.navbar_heading:
            self.change_current_tab("todos")
        else:
            self.change_current_tab("navbar")

    async def handle_help_key(self, event: events.Key):
        match event.key:
            case i if i in keys.move_down:
                await self.help_menu.key_down()
            case i if i in keys.move_up:
                await self.help_menu.key_up()
            case i if i in keys.move_to_top:
                await self.help_menu.key_home()
            case i if i in keys.move_to_bottom:
                await self.help_menu.key_end()

    async def on_key(self, event: events.Key) -> None:
        if (event.key in keys.show_help) or (event.key == "escape" and self.help):
            await self.toggle_help()
            return

        if self.help:
            await self.handle_help_key(event)
            return

        self.status_bar.clear_message()

        if self.current_tab == self.navbar_heading:
            await self.navbar.key_press(event)
        else:
            match self.current_status:
                case "SEARCH":
                    await self.search_tree.key_press(event)
                    self.status_bar.set_message(self.search_tree.search.render())

                case "SORT":
                    await self.sort_menu.key_press(event)

                case "NORMAL":
                    if event.key in keys.start_search:
                        await self.search_tree.set_values(self.todo_list.nodes)
                        await self.handle_change_status(
                            ChangeStatus(self, "SEARCH"),
                        )
                        await self.reset_screen()

                    elif event.key in keys.spawn_sort_menu:
                        await self.handle_change_status(
                            ChangeStatus(self, "SORT"),
                        )

                    else:
                        await self.todo_list.key_press(event)

                case _:
                    await self.todo_list.key_press(event)

        self.refresh(layout=True)

    # HANDLING EVENTS
    async def handle_change_status(self, event: ChangeStatus) -> None:
        status = event.status
        reset = (self.current_status in ["SEARCH", "SORT"]) or status == "SORT"
        self.current_status = status
        self.status_bar.set_status(status)

        if reset:
            await self.reset_screen()

        if status in ["NORMAL"]:
            self.change_current_tab(self.current_tab.name)

    async def handle_notify(self, event: Notify) -> None:
        self.status_bar.set_message(event.message)

    async def handle_list_item_selected(self, event: ListItemSelected) -> None:
        self.current_menu = event.selected
        await self.reset_screen()
        self.change_current_tab("todos" if event.focus else "navbar")

    async def handle_modify_topic(self, event: ModifyTopic) -> None:
        if event.old == event.new:
            return

        if event.old == "/" or event.old.endswith("//"):
            return

        self.todo_lists[event.new] = self.todo_lists.get(event.old, TodoList())

        if event.old in self.todo_lists:
            del self.todo_lists[event.old]

    async def handle_apply_sort_method(self, event: ApplySortMethod) -> None:
        await self.todo_list.sort_by(event.method)

    async def handle_highlight_node(self, event: HighlightNode) -> None:
        await self.todo_list.reach_to_node(event.id)

    async def handle_switch_tab(self, _: SwitchTab) -> None:
        self.switch_tabs()

    async def handle_remove_topic(self, event: RemoveTopic) -> None:
        for topic in list(self.todo_lists.keys()):
            if topic.startswith(event.selected):
                self.todo_lists.pop(topic, None)
