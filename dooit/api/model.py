from typing import Self
from typing import Any, List, Literal, TypeVar
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from .manager import manager

SortMethodType = Literal["description", "status", "due", "urgency", "effort"]
T = TypeVar("T")


class BaseModel(DeclarativeBase):
    pass


class BaseModelMixin:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class DooitModel(BaseModel, BaseModelMixin):
    """
    Model class to for the base tree structure
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_index: Mapped[int] = mapped_column(default=-1)

    @property
    def uuid(self) -> str:
        return f"{self.__class__.__name__}_{self.id}"

    @property
    def parent(self) -> Any:
        raise NotImplementedError

    @property
    def nest_level(self):
        level = 0
        parent = self.parent

        while (
            parent
            and isinstance(self, parent.__class__)
            and not getattr(parent, "is_root")
        ):
            level += 1
            parent = parent.parent

        return level

    @property
    def siblings(self) -> List[Any]:
        raise NotImplementedError

    @classmethod
    def from_id(cls, _id: str) -> Self:
        raise NotImplementedError

    def is_last_sibling(self) -> bool:
        return self.siblings[-1].id == self.id

    def is_first_sibling(self) -> bool:
        return self.siblings[0].id == self.id

    @property
    def has_same_parent_kind(self) -> bool:
        raise NotImplementedError

    def shift_up(self) -> bool:
        """
        Shift the item one place up among its siblings
        """

        if self.is_first_sibling():
            return False

        siblings = self.siblings
        index = siblings.index(self)
        siblings[index - 1].order_index += 1
        siblings[index].order_index -= 1

        siblings[index].save()
        siblings[index - 1].save()

        return True

    def shift_down(self) -> bool:
        """
        Shift the item one place down among its siblings
        """

        if self.is_last_sibling():
            return False

        siblings = self.siblings
        index = siblings.index(self)
        siblings[index + 1].order_index -= 1
        siblings[index].order_index += 1

        siblings[index].save()
        siblings[index + 1].save()

        return True

    def set_order_index(self, index: int) -> None:
        if index > len(self.siblings) or index < 0:
            index = len(self.siblings)

        siblings = [
            i for i in self.siblings if i.id != self.id and i.order_index >= index
        ]
        for i in siblings[::-1]:
            i.order_index += 1
            i.save()

        self.order_index = index
        self.save()

    def drop(self) -> None:
        manager.delete(self)

    def save(self) -> None:
        manager.save(self)
