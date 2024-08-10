from typing import TYPE_CHECKING, Any, List, Literal, Optional
from typing_extensions import Self
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from ._vars import session

SortMethodType = Literal["description", "status", "due", "urgency", "effort"]


class BaseModel(DeclarativeBase):
    pass


class BaseModelMixin:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


if TYPE_CHECKING:
    from dooit.api.workspace import Workspace
    from dooit.api.todo import Todo


class Model(BaseModel, BaseModelMixin):
    """
    Model class to for the base tree structure
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_index: Mapped[int] = mapped_column(default=-1)

    @property
    def parent(self) -> Any:
        return None

    @property
    def nest_level(self):
        level = 0
        parent = self.parent

        while parent and isinstance(self, parent.__class__):
            level += 1
            parent = parent.parent

        return level

    @property
    def siblings(self) -> List[Self]:
        query = (
            select(self.__class__)
            .where(self.__class__.parent == self.parent)
            .order_by(self.__class__.order_index)
        )
        return list(session.execute(query).scalars().all())

    @property
    def is_last_sibling(self) -> bool:
        return self.siblings[-1] == self

    @property
    def is_first_sibling(self) -> bool:
        return self.siblings[0] == self

    @property
    def has_same_parent_kind(self) -> bool:
        return isinstance(self.parent, self.__class__)

    def validate(self, key: str, value: str) -> bool:
        var = f"_{key}"
        if hasattr(self, var):
            return getattr(self, var).validate_value(value)
        else:
            return False

    def edit(self, key: str, value: str) -> None:
        """
        Edit item's attrs
        """

        var = f"_{key}"
        if hasattr(self, var):
            return getattr(self, var).set_value(value)

    def shift_up(self) -> None:
        """
        Shift the item one place up among its siblings
        """

        raise NotImplementedError

    def shift_down(self) -> bool:
        """
        Shift the item one place down among its siblings
        """

        raise NotImplementedError

    def prev_sibling(self) -> Optional[Self]:
        """
        Returns previous sibling item, if any, else None
        """

        raise NotImplementedError

    def next_sibling(self) -> Optional[Self]:
        """
        Returns next sibling item, if any, else None
        """

        raise NotImplementedError

    def add_sibling(self, inherit: bool = False) -> Self:
        """
        Add item sibling
        """

        raise NotImplementedError

        if self.parent:
            return self.parent.add_child(self.kind, self._get_index() + 1, inherit)
        else:
            raise TypeError("Cannot add sibling")

    def add_child(self, kind: str, index: int = 0, inherit: bool = False) -> Any:
        """
        Adds a child to specified index (Defaults to first position)
        """

        raise NotImplementedError

        from ..api.workspace import Workspace
        from ..api.todo import Todo

        if kind == "workspace":
            child = Workspace(parent=self)
        else:
            child = Todo(parent=self)
            if inherit and isinstance(self, Todo):
                child.fill_from_data(self.to_data(), overwrite_uuid=False)
                child._description.set_value("")
                child._effort._value = 0
                child.edit("status", "PENDING")

        children = self._get_children(kind)
        children.insert(index, child)

        return child

    def drop(self) -> None:
        session.delete(self)

    def save(self) -> None:
        session.add_all([self])
