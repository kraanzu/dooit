import re
from datetime import datetime, timedelta
from typing import List, Optional, Tuple
from yaml import safe_load
from pathlib import Path
from platformdirs import user_data_dir
from dooit.api import Todo, Workspace, manager
from rich.text import Text
from rich.console import Console

console = Console()
print = console.print
manager.register_engine()


def parse_recurrence(recurrence: str) -> timedelta:
    DURATION_LEGEND = {
        "m": "minute",
        "h": "hour",
        "d": "day",
        "w": "week",
    }

    def split_duration(duration: str) -> Tuple[str, str]:
        if re.match(r"^(\d+)[mhdw]$", duration):
            return duration[-1], duration[:-1]
        else:
            return tuple()

    sign, frequency = split_duration(recurrence)
    frequency = int(frequency)
    return timedelta(**{f"{DURATION_LEGEND[sign]}s": frequency})


def parse_due(due: str) -> Optional[datetime]:
    if due == "none":
        return None

    due_float = float(due)
    return datetime.fromtimestamp(due_float)


class Migrator2to3:
    old_location = XDG_DATA = Path(user_data_dir("dooit")) / "todo.yaml"

    def check_for_old_data(self):
        if not self.old_location.exists():
            return False

        return True

    def load_old(self):
        with self.old_location.open() as f:
            return safe_load(f)

    def migrate(self):
        print(
            Text("[?] ", style="bold yellow")
            + Text("Checking for old data ...", style="yellow")
        )

        if not self.check_for_old_data():
            print(
                Text("[-] ", style="bold red") + Text("No old data found", style="red")
            )
            return

        print(
            Text("[+] ", style="bold green")
            + Text("Found old data. Converting ... ", style="green")
        )

        data = self.load_old()
        for workspace in data:
            self.create_workspace(workspace)

    # ------------------------------------------------

    def create_workspace(self, data, parent=None):
        description = data.get("description")
        child_workspaces = data.get("workspaces", [])
        todos = data.get("todos", [])

        workspace = Workspace(description=description, parent_workspace=parent)
        workspace.save()

        for workspace in child_workspaces:
            self.create_workspace(workspace, parent=workspace)

        for todo in todos:
            self.create_todo(todo, parent_workspace=workspace)

    def create_todo(self, data: List, parent_todo=None, parent_workspace=None):
        self_data = data[0]
        if len(data) == 1:
            children_data = []
        else:
            children_data = data[1]

        description = self_data.get("description")
        pending = self_data.get("status") != "COMPLETED"
        urgency = self_data.get("urgency")
        due = self_data.get("due")
        effort = self_data.get("effort")
        recurrence = self_data.get("recurrence")

        todo = Todo(
            parent_todo=parent_todo,
            parent_workspace=parent_workspace,
            description=description,
            pending=pending,
            urgency=urgency,
            due=parse_due(due),
            effort=int(effort) if effort else None,
            recurrence=parse_recurrence(recurrence) if recurrence else None,
        )
        todo.save()

        for data in children_data:
            self.create_todo(
                data,
                parent_todo=todo,
            )


if __name__ == "__main__":
    m = Migrator2to3()
    if m.check_for_old_data():
        m.migrate()
