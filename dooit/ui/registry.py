from dooit.ui.api.components import WorkspaceLayout


class Registry:
    """
    Class to store global variables and objects
    """

    def __init__(self) -> None:
        self.workspace_layout = []

    def set_workspace_layout(self, layout: WorkspaceLayout):
        self.workspace_layout = layout

    def get_workspace_layout(self) -> WorkspaceLayout:
        return self.workspace_layout


registry = Registry()
