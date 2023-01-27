from typing import Dict
from dooit.api.workspace import Workspace
from .formatter import Formatter


class WorkspaceFormatter(Formatter):
    model_type = Workspace

    def style_desc(
        self,
        item: Workspace,
        is_highlighted: bool,
        is_editing: bool,
        kwargs: Dict[str, str],
    ) -> str:
        pass
        text = kwargs["desc"]

        if children := item.workspaces:
            text += self.format["children_hint"].format(count=len(children))

        return self.cursor_highlight(text, is_highlighted, is_editing)
