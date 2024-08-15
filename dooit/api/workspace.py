from typing import List, Optional
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from ..api.todo import Todo
from .model import Model
from .manager import manager


class Workspace(Model):

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

        with Session(manager.engine) as session:
            query = select(Workspace).where(Workspace.is_root == True)
            root = session.execute(query).scalars().first()

            if root is None:
                root = Workspace(is_root=True)
                session.add(root)
                session.commit()

            return root

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
        # query = (
        #     select(Workspace)
        #     .where(Workspace.parent_workspace_id == self.parent_workspace_id)
        #     .order_by(Workspace.order_index)
        # )
        # return list(manager.session.execute(query).scalars().all())

    def add_workspace(
        self,
        index: int = 0,
    ) -> "Workspace":
        workspace = Workspace(parent=self)
        workspace.save()
        return workspace

    def add_todo(
        self,
        index: int = 0,
    ) -> Todo:
        todo = Todo(parent=self)
        todo.save()
        return todo

    def save(self) -> None:
        if not self.parent_workspace and not self.is_root:
            root = self._get_or_create_root()
            self.parent_workspace = root

        return super().save()

    @classmethod
    def all(cls) -> List["Workspace"]:
        query = select(Workspace).where(Workspace.is_root == False)
        return list(manager.session.execute(query).scalars().all())
