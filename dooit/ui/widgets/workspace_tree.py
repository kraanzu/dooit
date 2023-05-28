from dooit.api.model import Model
from dooit.ui.events.events import SwitchTab, TopicSelect
from .tree import Tree


class WorkspaceTree(Tree):
    _empty = "workspace"

    def __init__(self, model: Model):
        super().__init__(model, "focus left-dock")

    async def watch_current(self, old: str | None, new: str | None):
        await super().watch_current(old, new)
        self.post_message(TopicSelect(self.node))

    async def switch_pane(self):
        if self.current:
            self.post_message(SwitchTab())
