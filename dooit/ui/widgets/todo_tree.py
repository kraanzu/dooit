from typing import Optional
from rich.table import Table
from rich.text import Text
from textual import events

from dooit.utils.conf_reader import Config

from .tree import Component, TreeList
from ...api.todo import Todo
from ...ui.events.events import SwitchTab
from ...api import Workspace

conf = Config()
EMPTY_TODO = conf.get("EMPTY_TODO")
dashboard = conf.get("dashboard")
PRINTABLE = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
COLUMN_ORDER = conf.get("COLUMN_ORDER")
format = conf.get("TODO")


class TodoTree(TreeList):
    """
    Tree structured Class to manage todos
    """

    options = Todo.fields
    EMPTY = dashboard
    model_kind = "todo"
    model_type = Todo

    def _get_children(self, model: Workspace):
        if model:
            return model.todos
        return []

    async def switch_tabs(self):
        if self.filter.value:
            await self._stop_filtering()

        await self.emit(SwitchTab(self))

    async def update_table(self, model: Optional[Workspace] = None):
        if not model:
            self.EMPTY = dashboard
            self.model = None
            self._refresh_rows()
        else:
            self.EMPTY = EMPTY_TODO
            if not self.item or not self.component:
                self.model = model
                self.current = -1
                self._refresh_rows()
            else:
                editing = self.editing
                path = self.item.path
                _old_val = ""

                if editing != "none":
                    _old_val = self.component.fields[editing].value
                    await self._cancel_edit()

                self.model = model
                self._refresh_rows()

                self.current = -1
                for i, j in enumerate(self.row_vals):
                    if j.item.path == path:
                        self.current = i
                        if editing != "none":
                            self.component.fields[editing].value = _old_val
                            await self.component.fields[editing].handle_keypress("end")
                            await self._start_edit(editing)
                        break

        self.refresh()

    def _setup_table(self) -> None:
        self.table = Table.grid(expand=True)
        for col in COLUMN_ORDER:
            if col == "desc":
                d = {"ratio": 1}
            elif col == "due":
                d = {"width": 20}
            elif col == "urgency":
                d = {"width": 1}
            else:
                raise TypeError

            self.table.add_column(col, **d)

    # ##########################################

    async def check_extra_keys(self, event: events.Key):

        key = (
            event.character
            if (event.character and (event.character in PRINTABLE))
            else event.key
        )

        if self.editing != "none":
            return
        if key in "d":
            await self._start_edit("due")
        elif key in "e":
            await self._start_edit("eta")
        elif key in "t":
            await self._start_edit("tags")
        elif key in "r":
            await self._start_edit("recur")
        elif key in "c":
            if self.item and self.component:
                self.item.toggle_complete()
        elif key in "+=":
            if self.component and self.item:
                self.item.increase_urgency()
        elif key in "_-":
            if self.component and self.item:
                self.item.decrease_urgency()

    def add_row(self, row: Component, highlight: bool) -> None:
        def colored(text, color):
            return f"[{color}]{text}[/{color}]"

        def status_color():
            status = row.item.status
            if status == "COMPLETED":
                return "b green"
            elif status == "PENDING":
                return "b yellow"
            else:
                return "b red"

        def stylize_desc(item: Todo, kwargs):  # noqa
            text = kwargs["desc"]

            # STATUS

            status_icon = item.status.lower() + "_icon"
            status_icon = format[status_icon]
            text = colored(status_icon, status_color()) + text

            # DESC
            if children := item.todos:
                d = {
                    "total": len(children),
                    "done": sum(i.status == "COMPLETED" for i in children),
                }
                d["remaining"] = d["total"] - d["done"]
                text += format["children_hint"].format(**d)

            # ETA
            if eta := kwargs["eta"]:
                color = format["eta_color"]
                icon = format["eta_icon"]
                text += colored(f" {icon}{eta}", color)

            # TAGS
            if tags := item.tags:
                tags = [i.strip() for i in kwargs["tags"].split(",")]
                icon = format["tags_icon"]
                seperator = format["tags_seperator"]
                color = format["tags_color"]
                t = f" {icon}"

                if seperator == "comma":
                    t += ", ".join(tags)
                elif seperator == "pipe":
                    t += " | ".join(tags)
                else:
                    t += f" {icon}".join(tags)

                text += colored(t, color)

            # RECURRENCE
            if recur := kwargs["recur"]:
                color = format["recurrence_color"]
                icon = format["recurrence_icon"]
                text += f"[{color}] {icon}{recur}[/{color}]"

            # COLORING
            if not highlight:
                color = format["dim"]
                text = len(format["pointer"]) * " " + text
            else:
                text = format["pointer"] + text
                if self.editing:
                    color = format["editing"]
                else:
                    color = format["highlight"]

            return colored(text, color)

        def stylize_due(item: Todo, kwargs):
            icon_color = status_color()
            text = colored(format["due_icon"], icon_color) + kwargs["due"]

            if not highlight:
                color = format["dim"]
            else:
                if self.editing:
                    color = format["editing"]
                else:
                    color = format["highlight"]

            return f"[{color}]{text}[/{color}]"

        def stylize_urgency(item: Todo, kwargs):
            val = item.urgency
            if val == 3:
                color = "orange1"
            elif val == 2:
                color = "yellow"
            elif val == 1:
                color = "green"
            else:
                color = "red"

            icon = f"urgency{val}_icon"
            icon = format[icon]

            return f"[{color}]{icon}[/{color}]"

        entry = []
        kwargs = {i: str(j.render()) for i, j in row.fields.items()}

        for column in COLUMN_ORDER:
            if column == "desc":
                res = stylize_desc(row.item, kwargs)
            elif column == "due":
                res = stylize_due(row.item, kwargs)
            elif column == "urgency":
                res = stylize_urgency(row.item, kwargs)
            else:
                continue

            if isinstance(res, str):
                res = res.format(**kwargs)
                res = Text.from_markup(res)
            else:
                res.plain = res.plain.format(**kwargs)
            entry.append(res)

        return self.push_row(entry, row.depth)
