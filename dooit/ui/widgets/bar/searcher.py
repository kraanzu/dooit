from dooit.ui.events.events import ChangeStatus
from dooit.ui.widgets.bar.status_bar import StatusBar
from dooit.ui.widgets.search_menu import SearchMenu
from dooit.ui.widgets.simple_input import Input
from dooit.utils.conf_reader import Config
from .status_bar_utils import StatusMiddle

BG = Config().get('BAR_BACKGROUND')


class Searcher(StatusMiddle, Input):
    DEFAULT_CSS = f"""
    Searcher {{
        padding-left: 1;
    }}
    """

    def __init__(self):

        super().__init__(classes="")
        self.styles.background = BG

    async def on_mount(self):
        from .status_bar import StatusBar

        self.app.query_one(StatusBar).set_status("SEARCH")

    async def on_unmount(self):
        from .status_bar import StatusBar

        self.app.query_one(StatusBar).set_status("NORMAL")

    async def keypress(self, key: str) -> None:
        if key == "escape":
            await self.app.query_one(SearchMenu).cancel_search()
            await self.app.query_one(StatusBar).replace_middle()

            self.remove()
            return

        if key == "enter":
            self.post_message(ChangeStatus("NORMAL"))
            await self.app.query_one(StatusBar).replace_middle()
            return

        await super().keypress(key)
        self.app.query_one(SearchMenu).apply_filter(self.value)
