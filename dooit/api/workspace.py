from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..api.todo import Todo
from .model import Model


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
        raise ValueError("Parent not found")

    def add_workspace(self, index: int = 0) -> "Workspace":
        workspace = Workspace(parent=self)
        workspace.save()
        return workspace

    def add_todo(self, index: int = 0) -> Todo:
        todo = Todo(parent=self)
        todo.save()
        return todo
