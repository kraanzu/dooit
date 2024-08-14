from typing import List, Optional, Self
from sqlalchemy import Connection, ForeignKey, select
from sqlalchemy import event
from sqlalchemy.orm import Mapped, Mapper, Session, mapped_column, relationship
from ..api.todo import Todo
from .model import Model
from ._vars import default_session


class Workspace(Model):

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_index: Mapped[int] = mapped_column(default=-1)
    description: Mapped[str] = mapped_column(default="")

    # --------------------------------------------------------------
    # ------------------- Relationships ----------------------------
    # --------------------------------------------------------------

    parent_workspace_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("workspace.id"), default=None
    )
    parent_workspace: Mapped[Optional["Workspace"]] = relationship(
        "Workspace", back_populates="workspaces", remote_side=[id]
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

    @property
    def parent(self) -> Optional["Workspace"]:
        return self.parent_workspace

    def get_siblings(self, session: Session = default_session) -> List[Self]:
        cls = self.__class__
        query = (
            select(cls)
            .where(cls.parent_workspace == self.parent_workspace)
            .order_by(cls.order_index)
        )
        return list(session.execute(query).scalars().all())

    def add_workspace(
        self,
        index: int = 0,
        session: Session = default_session,
    ) -> "Workspace":
        workspace = Workspace(parent=self)
        workspace.save(session)
        return workspace

    def add_todo(
        self,
        index: int = 0,
        session: Session = default_session,
    ) -> Todo:
        todo = Todo(parent=self)
        todo.save(session)
        return todo


@event.listens_for(Session, "before_commit")
def fix_order_id(session: Session):

    query = select(Workspace).where(Workspace.order_index == -1)
    objs = session.execute(query).scalars().all()

    for obj in objs:
        obj.order_index = len(obj.get_siblings(session))
