from typing import Type
from rich.console import RenderableType
from dooit.api.todo import Todo
from dooit.utils.conf_reader import Config
from .simple_input import SimpleInput

config = Config()
TODOS = config.get("TODO")
todo_editing = TODOS.get("editing")
todo_highlight = TODOS.get("highlight")
todo_dim = TODOS.get("dim")

WORKSPACES = config.get("WORKSPACE")
workspace_editing = WORKSPACES.get("editing")
workspace_highlight = WORKSPACES.get("highlight")
workspace_dim = WORKSPACES.get("dim")

RED = config.get("red")
YELLOW = config.get("yellow")
GREEN = config.get("green")
ORANGE = config.get("orange")

TODO_SELECTOR = "TodoWidget > ExpandedHorizontal > ExpandedHorizontal > Description"
WORKSPACE_SELCTOR = "WorkspaceWidget > Horizontal > Description"
DATE_MAX_WIDTH = 17


class Description(SimpleInput):
    DEFAULT_CSS = f"""
    Description {{
        width: auto;
        height: auto;
    }}

    {WORKSPACE_SELCTOR}.dim {{
        color: {workspace_dim};
    }}

    {WORKSPACE_SELCTOR}.highlight {{
        color: {workspace_highlight};
    }}

    {WORKSPACE_SELCTOR}.editing {{
        color: {workspace_editing};
    }}

    {TODO_SELECTOR}.dim {{
        color: {todo_dim};
    }}

    {TODO_SELECTOR}.highlight {{
        color: {todo_highlight};
    }}

    {TODO_SELECTOR}.editing {{
        color: {todo_editing};
    }}
    """


class Due(SimpleInput):
    DEFAULT_CSS = f"""
    Due {{
            width: {DATE_MAX_WIDTH};
        min-width: {DATE_MAX_WIDTH};
        max-width: {DATE_MAX_WIDTH};
    }}

    Due.dim {{
        color: {todo_dim}
    }}

    Due.highlight {{
        color: {todo_highlight}
    }}

    Due.editing {{
        color: {todo_editing}
    }}
    """

    def draw(self) -> str:
        icon = TODOS["due_icon"]
        value = super().draw()
        if not value:
            return ""

        return self._colorize_by_status(icon) + value


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


class Tags(SimpleInput):
    DEFAULT_CSS = f"""
    Tags {{
        color: {TODOS.get("tags_color")}
    }}
    """

    def draw(self) -> RenderableType:
        icon = " " + TODOS["tags_icon"]
        value = super().draw()
        if not value:
            return ""

        tags = [i.strip() for i in value.split(",")]
        tags = icon.join(tags)
        return icon + tags


class Status(SimpleInput):
    DEFAULT_CSS = f"""
    Status {{
        height: 1;
        width: auto;
    }}
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
