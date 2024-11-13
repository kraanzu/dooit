from datetime import datetime
from sqlalchemy import event, update
from ..todo import Todo


@event.listens_for(Todo, "before_update")
def update_pending_status_child(_, connection, target: Todo):
    to_update = []

    def update_children(todo: Todo):
        for child in todo.todos:
            to_update.append(child.id)
            update_children(child)

    # mark all siblings as completed
    update_children(target)
    query = update(Todo).where(Todo.id.in_(to_update)).values(pending=target.pending)
    connection.execute(query)


@event.listens_for(Todo, "before_update")
def update_pending_status_parent(mapper, connection, target: Todo):
    to_update_as_pending = []

    def update_parent_pending(todo: Todo):
        parent = todo.parent_todo
        if not parent:
            return

        to_update_as_pending.append(parent.id)
        update_parent_pending(parent)

    to_update_as_completed = []

    def update_parent_completed(todo: Todo):
        parent = todo.parent_todo
        if not parent:
            return

        all_sibling_completed = all([not sibling.pending for sibling in parent.todos])
        if all_sibling_completed:
            parent.pending = False
            to_update_as_completed.append(parent.id)
            update_parent_completed(parent)

    if target.pending:
        update_parent_pending(target)
        query = (
            update(Todo).where(Todo.id.in_(to_update_as_pending)).values(pending=True)
        )
    else:
        update_parent_completed(target)
        query = (
            update(Todo)
            .where(Todo.id.in_(to_update_as_completed))
            .values(pending=False)
        )

    connection.execute(query)


@event.listens_for(Todo, "before_update")
def update_due_for_recurrence(mapper, connection, todo: Todo):
    if todo.recurrence is None:
        return

    if todo.due is None:
        todo.due = datetime.now()

    if todo.pending:
        return

    todo.pending = True
    todo.due += todo.recurrence
