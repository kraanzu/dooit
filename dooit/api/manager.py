from .model import Model
from typing import Optional, Type
from ..utils import Parser


class Manager(Model):
    """
    Manager top class that manages basically
    """

    fields = []
    nomenclature: str = "Workspace"

    def __init__(self, name: str, parent: Optional["Model"] = None) -> None:
        from .workspace import Workspace

        super().__init__(name, parent)
        self.ctype: Type = Workspace

    def commit(self):
        """
        Save obj data generated
        """

        data = super().commit()
        Parser.save(data)

    def setup(self):
        """
        Load the storage file and re-create the tree
        """

        data = Parser.load()
        self.from_data(data)


manager = Manager(name="Manager")
manager.setup()
