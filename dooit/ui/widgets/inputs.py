from datetime import datetime, timedelta
from typing import Type
from rich.console import RenderableType
from dooit.api.model import Err, Result
from dooit.api.todo import Todo
from dooit.api.workspace import Workspace
from dooit.utils.conf_reader import config_man
from .simple_input import SimpleInput

TODOS = config_man.get("TODO")
WORKSPACES = config_man.get("WORKSPACE")


RED = config_man.get("red")
YELLOW = config_man.get("yellow")
GREEN = config_man.get("green")
ORANGE = config_man.get("orange")

DATE_FORMAT = config_man.get("DATE_FORMAT")
TIME_FORMAT = config_man.get("TIME_FORMAT")

DATE_MAX_WIDTH = 17


class Description(SimpleInput):
    DEFAULT_CSS = """
    Description {
        width: auto;
        height: auto;
    }
    """

    @property
    def empty_result(self) -> Result:
        return Err("Description cannot be empty!")

    def draw(self) -> str:
        model = self.model
        hint = ""

        if isinstance(model, Todo):
            if todos := model.todos:
                hint: str = TODOS["children_hint"]
                total = len(todos)
                done = sum(i.status == "COMPLETED" for i in todos)
                remaining = total - done
                hint = hint.format(
                    total=total,
                    done=done,
                    remaining=remaining,
                )
        elif isinstance(model, Workspace):
            if workspaces := model.workspaces:
                hint: str = WORKSPACES["children_hint"]
                params = {"count": len(workspaces)}
                hint = hint.format(**params)

        value = super().draw()
        if not value:
            return ""

        return value + hint


class Due(SimpleInput):
    DEFAULT_CSS = f"""
    Due {{
        width: {DATE_MAX_WIDTH};
        min-width: {DATE_MAX_WIDTH};
        max-width: {DATE_MAX_WIDTH};
    }}
    """

    def timedelta_to_words(self, delta: timedelta):
        is_negative = delta.total_seconds() <= 0
        if not is_negative:
            delta = delta + timedelta(days=1)

        days = abs(delta.days)

        years = days // 365
        months = (days % 365) // 30
        days = (days % 365) % 30
        hours, remainder = divmod(abs(delta.seconds), 3600)
        minutes, _ = divmod(remainder, 60)

        if years:
            return f"{years}yr" + f" {'ago' if is_negative else ''}"
        if months:
            return f"{months}mo" + f" {'ago' if is_negative else ''}"
        if days:
            return f"{days}d" + f" {'ago' if is_negative else ''}"

        time_parts = []
        if hours:
            time_parts.append(f"{hours}h")
        if minutes:
            time_parts.append(f"{minutes}min")

        if is_negative:
            time_parts.append("ago")

        return " ".join(time_parts) if time_parts else "0 min"

    def draw(self) -> str:
        icon = TODOS["due_icon"]
        style = getattr(self.screen, "date_style")

        due: datetime = getattr(self.model, f"_{self._property}")._value

        if self.is_editing:
            value = super().draw()
        else:
            if style == "classic":
                if not due:
                    return ""

                time = due.time()
                if time.hour == time.minute == 0:
                    value = due.strftime(DATE_FORMAT)
                else:
                    value = due.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")

            else:
                if not due:
                    return ""

                now = datetime.now()
                if not due.hour:
                    due = due.replace(day=due.day + 1)

                value = self.timedelta_to_words(due - now)

        return self._colorize_by_status(icon) + value

    def start_edit(self) -> None:
        self.value = ""
        return super().start_edit()


class Urgency(SimpleInput):
    def draw(self) -> str:
        urgency = int(self.model.urgency)
        icon = TODOS.get(f"urgency{urgency}_icon")
        if urgency == 1:
            color = GREEN
        elif urgency == 2:
            color = YELLOW
        elif urgency == 2:
            color = ORANGE
        else:
            color = RED

        return self._render_text_with_color(icon, color)


class Effort(SimpleInput):
    ModelType: Type[Todo]
    DEFAULT_CSS = f"""
    Effort {{
        color: {TODOS.get("effort_color")}
    }}
    """

    def draw(self) -> RenderableType:
        icon = TODOS["effort_icon"]
        value = super().draw()
        if not value:
            return ""

        return icon + value


class Status(SimpleInput):
    DEFAULT_CSS = """
    Status {
        height: 1;
        width: auto;
    }
    """

    def draw(self) -> str:
        status = super().draw().lower()
        icon = TODOS.get(f"{status}_icon")
        return self._colorize_by_status(icon)


class Recurrence(SimpleInput):
    DEFAULT_CSS = f"""
    Recurrence {{
        color: {TODOS.get("recurrence_color")}
    }}
    """

    def draw(self) -> RenderableType:
        icon = TODOS["recurrence_icon"]
        value = super().draw()
        if not value:
            return ""

        return icon + value
