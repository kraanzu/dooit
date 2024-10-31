<style>
h2 code {
    color: var(--vp-c-brand-1);
}
</style>

# Workspace

In this page, I'll lay out all the methods available on the workspace class

:::tip :bulb: TIP
As mentioned in the introduction, `Workspace` class is a table and any sql operations can be performed using sqlalchemy
:::

<!-- ----------------------- ATTRIBUTES ---------------------------------- -->

## `attr`  description

The description of the workspace

```python
description: Mapped[str] = mapped_column(default="")
```

## `attr`  parent_workspace

The parent workspace of the workpsace

```python
parent_workspace: Mapped[Optional["Workspace"]] = relationship(
    "Workspace",
    back_populates="workspaces",
    remote_side=[id],
)
```

## `attr`  workspaces

The child workspaces of the workspace

```python
workspaces: Mapped[List["Workspace"]] = relationship(
    "Workspace",
    back_populates="parent_workspace",
    cascade="all",
    order_by="Workspace.order_index",
)
```

## `attr` todos

The todos for the workspace

```python
todos: Mapped[List["Todo"]] = relationship(
    "Todo",
    back_populates="parent_workspace",
    cascade="all, delete-orphan",
    order_by="Todo.order_index",
)
```

<!-- --------------------- CLASSMETHODS ----------------------------------- -->

## `classmethod` from_id

```python
from_id(id: str | int) -> Workspace
```

Returns the workspace object with the given id

**Parameters:**

| Param|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| id            |                     | The id of the workspace object you want to get                                           |

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| Self          |                     | The workspace object                                                                     |

**Raises:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| ValueError    |                     | If an invalid ID is passed                                                               |


## `classmethod` all

```python
all() -> List[Workspace]
```

Returns all the workspaces from the database

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| List[Self]    |                     | List of the workspaces present in the database                                           |

<!-- ---------------- PROPERTIES ------------------------------------- -->

## `property` parent

```python
parent -> Workspace
```

Returns the parent of the workspace object

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| Workspace     |                     | The parent of the workspace object                                                       |

## `property` nest_level

```python
nest_level -> int
```

Returns the nested level from the root

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| int           |                     | Depth of the nesting                                                                     |


<!-- ------------------ METHODS -------------------------------------- -->

## `method` siblings

```python
siblings() -> List[Workspace]
```

Returns the siblings for the workspace (including self)

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| List[Self]    |                     | List of the siblings (including self)                                                    |


## `method` sort_siblings


```python
sort_siblings()
```

Sorts all the siblings ***(by description)***


## `method` add_todo

```python
add_todo() -> Todo
```

Adds a todo to the workspace object

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| Todo          |                     | The newly added todo                                                                     |


## `method` add_workspace

```python
add_workspace() -> Workspace
```

Adds a child workspace to the workspace object

**Returns:**

| Type|<div style="width: 100px">Default</div> |Description|
| ------------- | :----------------:  | :----------------------------------------------------------------------------------------|
| Workspace     |                     | The newly added Workspace                                                                |

## `method` shift_down

Shifts the workspace down by one index (Nothing happens if its the first workspace)

```python
shift_down()
```

## `method` shift_up

Shifts the workspace down by one index (Nothing happens if its the last workspace)

```python
shift_up()
```

## `method` save

Saves any modifications done on the attributes to the database

```python
save()
```

