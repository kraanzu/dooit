import faker
from random import randint
from dooit.api import Todo, Workspace, manager

manager.register_engine()

f = faker.Faker()


def gen_todo(parent):
    words = randint(2, 9)
    description = " ".join(f.words(nb=words))
    due = f.date_time()
    urgency = randint(2, 5) if randint(0, 10) == 5 else 1

    todo = Todo(
        description=description,
        due=due,
        urgency=urgency,
        pending=randint(1, 3) == 3,
    )

    if isinstance(parent, Todo):
        todo.parent_todo = parent
    else:
        todo.parent_workspace = parent

    todo.save()
    return todo


def gen_todos(parent, count):
    return [gen_todo(parent) for _ in range(count)]


def gen_workspace(parent=None):
    words = randint(1, 2)
    description = " ".join(f.words(nb=words))

    workspace = Workspace(description=description, parent_workspace=parent)
    workspace.save()

    return workspace


w1 = gen_workspace()
w1_childs = [gen_workspace(w1) for _ in range(5)]

w2 = gen_workspace()
w3 = gen_workspace()


t1 = gen_todos(w1, 5)
gen_todos(t1[0], 7)
gen_todos(t1[3], 3)

_ = [gen_todos(w, randint(1, 20)) for w in w1_childs]
gen_todos(w2, 20)
gen_todos(w3, 30)
