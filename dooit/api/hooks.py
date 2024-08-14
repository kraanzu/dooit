from typing import Type, Union
from sqlalchemy.orm import Session
from sqlalchemy import select, event

from .workspace import Workspace
from .todo import Todo


@event.listens_for(Session, "before_commit")
def fix_order_id(session: Session):

    def fix(cls: Union[Type[Workspace], Type[Todo]]):
        query = select(cls).where(cls.order_index == -1)
        objs = session.execute(query).scalars().all()

        for obj in objs:
            obj.order_index = len(obj.get_siblings(session))

    fix(Workspace)
    fix(Todo)
