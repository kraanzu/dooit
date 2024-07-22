from dooit.api.model import Err, Result
from .simple_input import SimpleInput


class TodoDescription(SimpleInput):
    _property = "description"

    @property
    def empty_result(self) -> Result:
        return Err("Description cannot be empty!")


class WorkspaceDescription(SimpleInput):
    _property = "description"

    @property
    def empty_result(self) -> Result:
        return Err("Description cannot be empty!")


class Due(SimpleInput):
    def start_edit(self) -> None:
        self.value = ""
        return super().start_edit()

    # def timedelta_to_words(self, delta: timedelta):
    #     is_negative = delta.total_seconds() <= 0
    #     if not is_negative:
    #         delta = delta + timedelta(days=1)
    #
    #     days = abs(delta.days)
    #
    #     years = days // 365
    #     months = (days % 365) // 30
    #     days = (days % 365) % 30
    #     hours, remainder = divmod(abs(delta.seconds), 3600)
    #     minutes, _ = divmod(remainder, 60)
    #
    #     if years:
    #         return f"{years}yr" + f" {'ago' if is_negative else ''}"
    #     if months:
    #         return f"{months}mo" + f" {'ago' if is_negative else ''}"
    #     if days:
    #         return f"{days}d" + f" {'ago' if is_negative else ''}"
    #
    #     time_parts = []
    #     if hours:
    #         time_parts.append(f"{hours}h")
    #     if minutes:
    #         time_parts.append(f"{minutes}min")
    #
    #     if is_negative:
    #         time_parts.append("ago")
    #
    #     return " ".join(time_parts) if time_parts else "0 min"
    #
    # def draw(self) -> str:
    #     icon = TODOS["due_icon"]
    #     style = "classic"
    #
    #     due: datetime = getattr(self.model, f"_{self._property}")._value
    #
    #     if self.is_editing:
    #         value = super().draw()
    #     else:
    #         if style == "classic":
    #             if not due:
    #                 return ""
    #
    #             time = due.time()
    #             if time.hour == time.minute == 0:
    #                 value = due.strftime(DATE_FORMAT)
    #             else:
    #                 value = due.strftime(f"{DATE_FORMAT} {TIME_FORMAT}")
    #
    #         else:
    #             if not due:
    #                 return ""
    #
    #             now = datetime.now()
    #             if not due.hour:
    #                 due += timedelta(days=1)
    #
    #             value = self.timedelta_to_words(due - now)
    #
    #     return icon + value


class Urgency(SimpleInput): ...


class Effort(SimpleInput): ...


class Status(SimpleInput): ...


class Recurrence(SimpleInput): ...
