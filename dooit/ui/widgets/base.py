from textual.widget import Widget
from dooit.ui.events.events import ChangeStatus, StatusType


class HelperWidget(Widget):
    """
    Helper Widgets to Tree Widgets
    Currently base for `SortOptions` and `SearchMenu`
    """

    DEFAULT_CSS = """
    HelperWidget {
        layer: L1;
        display: none;
    }
    """

    _status: StatusType

    async def hide(self) -> None:
        self.styles.layer = "L1"
        self.display = False
        self.post_message(ChangeStatus("NORMAL"))

    async def start(self) -> None:
        self.styles.layer = "L4"
        self.display = True
        self.post_message(ChangeStatus(self._status))

    async def cancel(self) -> None:
        await self.hide()

    async def stop(self):
        pass
