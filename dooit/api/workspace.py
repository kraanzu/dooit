from typing import List, Optional, Union, Self
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from ..api.todo import Todo
from .model import DooitModel
from .manager import manager

ModelType = Union["Workspace", "Todo"]
ModelTypeList = Union[List["Workspace"], List["Todo"]]


class Workspace(DooitModel):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_index: Mapped[int] = mapped_column(default=-1)
    description: Mapped[str] = mapped_column(default="")
    is_root: Mapped[bool] = mapped_column(default=False)

    # --------------------------------------------------------------
    # ------------------- Relationships ----------------------------
    # --------------------------------------------------------------

    parent_workspace_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("workspace.id"), default=None
    )
    parent_workspace: Mapped[Optional["Workspace"]] = relationship(
        "Workspace",
        back_populates="workspaces",
        remote_side=[id],
    )

    workspaces: Mapped[List["Workspace"]] = relationship(
        "Workspace",
        back_populates="parent_workspace",
        cascade="all",
    )
    todos: Mapped[List["Todo"]] = relationship(
        "Todo",
        back_populates="parent_workspace",
        cascade="all, delete-orphan",
    )

    @classmethod
    def _get_or_create_root(cls) -> "Workspace":

        query = select(Workspace).where(Workspace.is_root == True)
        root = manager.session.execute(query).scalars().first()

        if root is None:
            root = Workspace(is_root=True)
            root.save()

        return root

    @classmethod
    def from_id(cls, _id: str) -> "Workspace":
        _id = _id.lstrip("Workspace_")
        query = select(Workspace).where(Workspace.id == _id)
        res = manager.session.execute(query).scalars().first()
        assert res is not None
        return res

    @property
    def parent(self) -> Optional["Workspace"]:
        return self.parent_workspace

    @property
    def has_same_parent_kind(self) -> bool:
        return self.parent is not None

    @property
    def siblings(self) -> List["Workspace"]:

        if not self.parent_workspace:
            return []

        assert not self.is_root

        return sorted(
            self.parent_workspace.workspaces, key=lambda x: x.order_index or -1
        )

    def _insert(self, items: ModelTypeList, obj: ModelType, index: int) -> None:
        children = [i for i in items if i.order_index or -1 >= index]
        for child in children[::-1]:
            child.order_index += 1
            child.save()

        obj.order_index = index
        obj.save()

    def add_workspace(self) -> "Workspace":
        workspace = Workspace(parent_workspace=self)
        workspace.save()
        return workspace

    def add_todo(self) -> "Todo":
        todo = Todo(parent_workspace=self)
        todo.save()
        return todo

    def add_sibling(self) -> "Workspace":
        assert self.parent_workspace is not None

        workspace = self.parent_workspace.add_workspace()
        workspace.set_order_index(self.order_index + 1)
        return workspace

    def save(self) -> None:
        if not self.parent_workspace and not self.is_root:
            root = self._get_or_create_root()
            self.parent_workspace = root

        return super().save()

    @classmethod
    def all(cls) -> List["Workspace"]:
        query = select(Workspace).where(Workspace.is_root == False)
        return list(manager.session.execute(query).scalars().all())
