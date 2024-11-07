# Dooit Vars

This api component exposes some of the stuff running on dooit + act as a global register to tweak settings \
Its still developing and I'll add more stuff to it as per demand!

### theme

Returns the current theme object (see [theme](../configuration/theme.md))

```py{6}
from dooit.ui.api.events import DooitEvent
from dooit.ui.api import DooitAPI, subscribe

@subscribe(DooitEvent)
def foo(api: DooitAPI, event: DooitEvent):
    theme = api.vars.theme
```

### current_workspace

Returns the current current workspace object of the highlighted workspacec (see [workspace](../backend/workspace.md))

```py{6}
from dooit.ui.api.events import DooitEvent
from dooit.ui.api import DooitAPI, subscribe

@subscribe(DooitEvent)
def foo(api: DooitAPI, event: DooitEvent):
    current_workspace = api.vars.current_workspace
```
