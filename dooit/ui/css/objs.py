"""
CSS File for python classses
"""

from . import conf

BG = conf.get("BACKGROUND")
DIM = conf.get("BORDER_DIM")


OBJS = f"""
Screen {{
    background: {BG};
    layout: grid;
    grid-size: 2 2;
    grid-columns: 2fr 8fr;
    grid-rows: 1fr 1;
}}

HelpScreen {{
    layout: vertical;
    scrollbar-size: 1 1;
}}

WorkspaceTree, TodoTree, EmptyWidget {{
    border: blank;
    padding: 1;
    background: #242831;
}}

SortOptions {{
    content-align: center middle;
}}

SimpleInput, Pointer{{
    height: auto;
    width: auto;
}}

Horizontal {{
    height: auto;
    width: 100%;
}}

StatusBar {{
    column-span: 2;
}}

WorkspaceWidget, TodoWidget {{
    height: auto;
}}

Vertical {{
    height: 100%;
    width: 100%;
    column-span: 2;
    row-span: 2;
    scrollbar-size: 1 1;
}}

"""
