# Dooit Formatters

## What are formatters?

Formatters are, _simply put_, functions to modify the content you're seeing by default on dooit

For example, by default you see the `due` column values in format DD-MM-YYY but if you'd want to change it, you can use a formatter

Some of the reasons you might use a formatter:

- `styling text`
- `adding extra info`

You can find a [a wide range of formatters](https://dooit-org.github.io/dooit-extras/formatters/description.html) in dooit extras

## Creating formatters

For creating a formatter, you define a function which takes in:

- `value` -> The real value of the object (for e.g., `due` will be a `datetime` object, `description` will be a `str`)
- `model` -> The respective `Todo` or `Workspace` object
- `api` [Optional] -> The dooit api 

:::info :grey_exclamation: NOTE
`api` paramater is optional and can be excluded if not necessary
:::

### An example formatter to format due into a readable format:

```python
from datetime import datetime
from dooit.api import Todo

def my_custom_due(due: datetime, model: Todo):
    if due.year != datetime.today().year:
        return due.strftime("%b %d, %Y")
    else:
        return due.strftime("%b %d")
```

For example the date is `30-12-2024`, then this function will return `Dec 30, 2024` if the current year is not 2024 else `Dec 30`

### An example formatter to highlight all words in description that starts with `!` symbol

```python
from dooit.api import Todo
from dooit.ui.api import DooitAPI
from rich.text import Text

def redify_important(description: str, model: Todo, api: DooitAPI):
    regex = r"!([\w]+)"
    text = Text(description)
    text.highlight_regex(regex, style = api.vars.theme.red)
    return text
```

## Using formatters

## Combining formatters
