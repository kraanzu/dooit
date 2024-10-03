from sqlalchemy import event
from ..workspace import Workspace
from ..todo import Todo


@event.listens_for(Workspace, "before_update")
@event.listens_for(Workspace, "before_insert")
def fix_order_id_workspace(mapper, connection, target: Workspace):
    if target.is_root:
        return

    if target.order_index is None or target.order_index == -1:
        target.order_index = len(target.siblings) - 1


@event.listens_for(Todo, "before_insert")
@event.listens_for(Todo, "before_update")
def fix_order_id_todo(mapper, connection, target: Todo):
    if target.order_index is None or target.order_index == -1:
        target.order_index = len(target.siblings) - 1
