class Registry:
    """
    Class to store global variables and objects
    """

    def __init__(self) -> None:
        self.variables = {}

    def set_workspace_layout(self, layout):
        self.variables["workspace_layout"] = layout


registry = Registry()
