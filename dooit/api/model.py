from typing import Any, List, Literal, Optional
from typing_extensions import Self
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from sqlalchemy.ext.declarative import declared_attr
from ._vars import default_session

SortMethodType = Literal["description", "status", "due", "urgency", "effort"]


class BaseModel(DeclarativeBase):
    pass


class BaseModelMixin:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class Model(BaseModel, BaseModelMixin):
    """
    Model class to for the base tree structure
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_index: Mapped[int] = mapped_column(default=-1)

    @property
    def parent(self) -> Any:
        raise NotImplementedError

    @property
    def nest_level(self):
        level = 0
        parent = self.parent

        while parent and isinstance(self, parent.__class__):
            level += 1
            parent = parent.parent

        return level

    def get_siblings(self, session: Session = default_session) -> List[Self]:
        raise NotImplementedError

    def is_last_sibling(self, session: Session = default_session) -> bool:
        return self.get_siblings(session)[-1] == self

    def is_first_sibling(self, session: Session = default_session) -> bool:
        return self.get_siblings(session)[0] == self

    @property
    def has_same_parent_kind(self) -> bool:
        raise NotImplementedError

    def shift_up(self, session: Session = default_session) -> bool:
        """
        Shift the item one place up among its siblings
        """

        if self.is_first_sibling(session):
            return False

        siblings = self.get_siblings(session)
        index = siblings.index(self)
        siblings[index - 1].order_index = index
        siblings[index].order_index = index - 1

        siblings[index].save()
        siblings[index - 1].save()

        return True

    def shift_down(self, session: Session = default_session) -> bool:
        """
        Shift the item one place down among its siblings
        """

        if self.is_last_sibling(session):
            return False

        siblings = self.get_siblings(session)
        index = siblings.index(self)
        siblings[index + 1].order_index = index
        siblings[index].order_index = index + 1

        siblings[index].save(session)
        siblings[index + 1].save(session)

        return True

    def add_sibling(
        self, inherit: bool = False, session: Session = default_session
    ) -> Self:
        """
        Add item sibling
        """

        raise NotImplementedError

        if self.parent:
            return self.parent.add_child(self.kind, self._get_index() + 1, inherit)
        else:
            raise TypeError("Cannot add sibling")

    def drop(self, session: Session = default_session) -> None:
        session.delete(self)
        session.commit()

    def save(self, session: Session = default_session) -> None:
        session.add_all([self])
        session.commit()
