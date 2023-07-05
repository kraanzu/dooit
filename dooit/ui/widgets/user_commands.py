from abc import ABC
from typing import Optional
from dooit.ui.events.events import SwitchTab
from dooit.ui.widgets.tree import SearchEnabledError

#//===========================  Command pattern
class Command(ABC):
    """
    Interface that defines what a user command is for the Invoker to use
    """
    async def execute(self):
        pass

# //===========================  Concrete Commands
class AddSiblingCommand(Command):
    def __init__(self, tree) -> None:
        self.tree = tree

    async def execute(self):
        if self.tree.filter.value:
            raise SearchEnabledError

        if self.tree.current == -1:
            sibling = self.tree._add_child()
        else:
            sibling = self.tree._add_sibling()

        self.tree._refresh_rows()
        await self.tree._move_to_item(sibling, "description") # TODO: TRY to make the command do this line

class AddChildCommand(Command):
    def __init__(self, tree) -> None:
        self.tree = tree

    async def execute(self):
        if self.tree.filter.value:
            raise SearchEnabledError

        if self.tree.current != -1:
            self.tree.component.expand()

        child = self.tree._add_child()
        self.tree._refresh_rows()
        await self.tree._move_to_item(child, "description")

class RemoveItemCommand(Command):
    def __init__(self, tree, move_cursor_up: bool = False) -> None:
        self.tree = tree
        self.move_cursor_up: bool = move_cursor_up

    async def execute(self):
        commit = self.tree.item.description != ""
        self.tree._drop()
        self.tree._refresh_rows()
        self.tree.current -= self.move_cursor_up
        if commit:
            self.tree.commit()

class StartSearchCommand(Command):
    def __init__(self, tree) -> None:
        self.tree = tree

    async def execute(self):
        self.tree.filter.on_focus()
        await self.tree.notify(self.tree.filter.render())
        await self.tree.change_status("SEARCH")

class StopSearchCommand(Command):
    def __init__(self, tree, clear: bool = True) -> None:
        self.tree = tree
        self.clear: bool = clear

    async def execute(self):
        if self.clear:
            self.tree.filter.clear()

        self.tree.filter.on_blur()
        self.tree._refresh_rows()
        await self.tree.notify(self.tree.filter.render())
        await self.tree.change_status("NORMAL")

class StartEditCommand(Command):
    def __init__(self, tree, field: Optional[str]) -> None:
        self.tree = tree
        self.field: Optional[str] = field

    async def execute(self):
        if not self.field or self.field == "none":
            return

        if self.field not in self.tree.component.fields.keys():
            await self.tree.notify(
                f"[yellow]Can't change [b orange1]`{self.field}`[/b orange1] here![/yellow]"
            )
            return

        if self.field == "description":
            await self.tree.change_status("INSERT")
        elif self.field == "due":
            await self.tree.change_status("DATE")

        ibox = self.tree.component.fields[self.field]
        ibox.value = getattr(self.tree.item, f"{self.field}")

        ibox.move_cursor_to_end()  # starting a new edit
        self.tree.component.fields[self.field].on_focus()
        self.tree.editing = self.field

class StopEditCommand(Command):
    def __init__(self, tree, edit: bool = True) -> None:
        self.tree = tree
        self.edit: bool = edit

    async def execute(self):
        if self.tree.editing == "none" or self.tree.current == -1:
            return

        editing = self.tree.editing
        simple_input = self.tree.component.fields[editing]
        old_val = getattr(self.tree.component.item, self.tree.editing)

        if not self.edit:
            simple_input.value = old_val

        res = self.tree.component.item.edit(self.tree.editing, simple_input.value)

        await self.tree.notify(res.text())
        if not res.ok:
            if res.cancel_op:
                # REMOVE self.invoker and use self.tree.invoker
                await self.tree.invoker.execute_command(RemoveItemCommand(self.tree, True))
            await self.tree._current_change_callback()
        else:
            self.tree.commit()

        simple_input.on_blur()
        if self.tree.current != -1:
            self.tree.component.refresh()
 
        self.tree.editing = "none"
        await self.tree.change_status("NORMAL")

        if self.edit and not old_val and editing == "description":
            await self.tree.invoker.add_sibling()

class ToggleExpandCommand(Command):
    def __init__(self, tree) -> None:
        self.tree = tree

    async def execute(self):
        self.tree.component.toggle_expand()
        self.tree._refresh_rows()

class ToggleExpandParentCommand(Command):
    def __init__(self, tree) -> None:
        self.tree = tree

    async def execute(self):
        parent = self.tree.item.parent
        if not parent:
            return

        if parent.path in self.tree._rows:
            index = self.tree._rows[parent.path].index
            self.tree.current = index

            await self.tree.invoker.execute_command(ToggleExpandCommand(self.tree))
            # await self.tree.toggle_expand()

class SwitchPaneCommand(Command):
    def __init__(self, tree) -> None:
        self.tree = tree

    async def execute(self):
        if self.tree.model_kind == "workspace":
            if self.tree.current == -1:
                return

            if self.tree.filter.value:
                if self.tree.current != -1:
                    await self.tree._current_change_callback()

                await self.tree.invoker.stop_search()
                self.tree.current = -1
            self.tree.post_message(SwitchTab())

        elif self.tree.model_kind == "todo":
            if self.tree.filter.value:
                await self.tree.invoker.stop_search()

            self.tree.post_message(SwitchTab())

class SortCommand(Command):
    def __init__(self, tree, attr: str) -> None:
        self.tree = tree
        self.attr = attr

    def execute(self):
        curr = self.tree.item.path
        self.tree.item.sort(self.attr)
        self.tree._refresh_rows()
        self.tree.current = self.tree._rows[curr].index
        self.tree.commit()

class ShiftUpCommand(Command):
    def __init__(self, tree) -> None:
        self.tree = tree

    async def execute(self):
        self.tree._shift_up()
        await self.tree.move_up()
        self.tree._refresh_rows()
        self.tree.commit()

class ShiftDownCommand(Command):
    def __init__(self, tree) -> None:
        self.tree = tree

    async def execute(self):
        self.tree._shift_down()
        await self.tree.move_down()
        self.tree._refresh_rows()
        self.tree.commit()

# //===========================  Invoker
class Invoker:
    """
    Class that performs the user commands that are requested by the "handle_key" function from TreeList
    Invoker performs all the user commands through its "execute_command" function, using inheritance
    from the abstract command
    """

    def __init__(self, tree) -> None:
        self.tree = tree
        self.user_commands = ["add_sibling"
            , "add_child"
            , "start_edit"
            , "start_search"
            , "stop_search"
            , "remove_item"
            , "toggle_expand"
            , "toggle_expand_parent"
            , "stop_edit"
            , "switch_pane"
            , "shift_up"
            , "shift_down"
            ]

    def noasync_execute_command(self, command: Command):
        command.execute()

    async def execute_command(self, command: Command):
        await command.execute()

    async def add_sibling(self) -> None:
        command = AddSiblingCommand(self.tree)
        await self.execute_command(command)

    async def add_child(self) -> None:
        command = AddChildCommand(self.tree)
        await self.execute_command(command)

    async def remove_item(self, move_cursor_up: bool = False) -> None:
        command = RemoveItemCommand(self.tree, move_cursor_up)
        await self.execute_command(command)

    async def start_search(self) -> None:
        command = StartSearchCommand(self.tree)
        await self.execute_command(command)

    async def stop_search(self, clear: bool = True) -> None:
        command = StopSearchCommand(self.tree, clear)
        await self.execute_command(command)

    async def start_edit(self, field: Optional[str]) -> None:
        command = StartEditCommand(self.tree, field)
        await self.execute_command(command)

    async def stop_edit(self, edit: bool = True) -> None:
        command = StopEditCommand(self.tree, edit)
        await self.execute_command(command)
        
    async def toggle_expand(self) -> None:
        command = ToggleExpandCommand(self.tree)
        await self.execute_command(command)

    async def toggle_expand_parent(self) -> None:
        command = ToggleExpandParentCommand(self.tree)
        await self.execute_command(command)

    async def switch_pane(self) -> None:
        await self.execute_command(SwitchPaneCommand(self.tree))

    def sort(self, attr: str) -> None:
        self.noasync_execute_command(SortCommand(self.tree, attr))
        
    async def shift_up(self) -> None:
        await self.execute_command(ShiftUpCommand(self.tree))

    async def shift_down(self) -> None:
        await self.execute_command(ShiftDownCommand(self.tree))
        