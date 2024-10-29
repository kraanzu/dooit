# Setting up Keys

Setting up keys in dooit is pretty straightforward

## Basic key binding

Key manager is available via api's `keys` variable and the general method looks something like this:

```python
api.keys.set(keybind, callback, description, group)
```

Example: 

```python
api.keys.set("j", api.move_down, "my custom vim keys")
api.keys.set("k", api.move_up, "my custom vim keys")
```

where `description` and `group` are optional

This would show up in the help menu like this:

![Keybind Preview 1](./imgs/keybind_preview_1.png)

## Multiple key binding

If you'd like to set multiple keybinding for same function, you can separate them by comma

For example, you'd like to use `+/-` keys for increasing or decreasing urgency but on QWERTY US layout, the `+` key needs shift as well
So you could set something like this:

```python
api.keys.set("=,+", api.increase_urgency)
api.keys.set("-,_", api.decrease_urgency)
```

::: tip ***ADVANCED:***
You can also pass custom functions as callbacks
Check out [Backend API](/backend/workspace)
:::
