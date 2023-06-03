from typing import Literal, Optional, Type
from dooit.api.model import Model
from dooit.ui.events.events import SwitchTab, TopicSelect
from dooit.ui.widgets.workspace import WorkspaceWidget
from .tree import Tree


class WorkspaceTree(Tree):
    _empty = "workspace"

    def __init__(self, model: Model):
        super().__init__(model, "focus left-dock")

    @property
    def widget_type(self) -> Type[WorkspaceWidget]:
        return WorkspaceWidget

    async def watch_current(self, old: Optional[str], new: Optional[str]):
        await super().watch_current(old, new)
        self.post_message(TopicSelect(None if not new else self.node))

    async def switch_pane(self):
        if self.current:
            self.post_message(SwitchTab())

    @property
    def model_class_kind(self) -> Literal["workspace"]:
        return "workspace"
