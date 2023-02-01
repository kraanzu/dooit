from typing import Dict
from dooit.api import Todo
from .formatter import Formatter


class TodoFormatter(Formatter):
    model_type = Todo

    def status_color(self, todo: Todo):
        status = todo.status
        if status == "COMPLETED":
            return "b green"
        elif status == "PENDING":
            return "b yellow"
        else:
            return "b red"

    def style_description(
        self,
        item: model_type,
        is_highlighted: bool,
        is_editing: bool,
        kwargs: Dict[str, str],
    ) -> str:
        text = kwargs["description"]

        # STATUS ICON
        status_icon = item.status.lower() + "_icon"
        status_icon = self.format[status_icon]
        text = self.colored(status_icon, self.status_color(item)) + text

        # DESCRIPTION
        if children := item.todos:
            d = {
                "total": len(children),
                "done": sum(i.status == "COMPLETED" for i in children),
                "remaining": sum(i.status != "COMPLETED" for i in children),
            }
            text += self.format["children_hint"].format(**d)

        # TAGS
        if tags := kwargs["tags"]:
            tags = [i.strip() for i in kwargs["tags"].split(",")]
            icon = self.format["tags_icon"]
            seperator = self.format["tags_seperator"]
            color = self.format["tags_color"]
            t = f" {icon}"

            if seperator == "comma":
                t += ", ".join(tags)
            elif seperator == "pipe":
                t += " | ".join(tags)
            else:
                t += f" {icon}".join(tags)

            text += self.colored(t, color)

        # RECURRENCE
        if recurrence := kwargs["recurrence"]:
            color = self.format["recurrence_color"]
            icon = self.format["recurrence_icon"]
            text += f"[{color}] {icon}{recurrence}[/{color}]"

        return self.cursor_highlight(text, is_highlighted, is_editing)

    def style_due(
        self,
        item: model_type,
        is_highlighted: bool,
        is_editing: bool,
        kwargs: Dict[str, str],
    ) -> str:
        icon_color = self.status_color(item)
        text = self.colored(self.format["due_icon"], icon_color) + kwargs["due"]

        return self.cursor_highlight(text, is_highlighted, is_editing)

    def style_urgency(
        self,
        item: model_type,
        is_highlighted: bool,
        is_editing: bool,
        kwargs: Dict[str, str],
    ) -> str:
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
        icon = self.format[icon]

        return self.colored(icon, color)
