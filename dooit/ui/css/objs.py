"""
CSS File for python classses
"""

from . import conf

BG = conf.get("BACKGROUND")
DIM = conf.get("BORDER_DIM")
BORDER_TITLE_DIM = conf.get("BORDER_TITLE_DIM")

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
    background: {BG};
    border: {DIM};
    border-title-background: {DIM};
    border-title-color: {BORDER_TITLE_DIM};
    padding: 1;
    width: 100%;
    height: 100%;
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
