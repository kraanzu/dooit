"""
CSS File for python classes
"""

from . import conf

BG = conf.get("BACKGROUND")
DIM = conf.get("BORDER_DIM")
BORDER_TITLE_DIM = conf.get("BORDER_TITLE_DIM")
if not isinstance(BORDER_TITLE_DIM, tuple):
    BORDER_TITLE_DIM = BORDER_TITLE_DIM, DIM

TODOS_BG = conf.get("TODOS_BACKGROUND")
WORKSPACES_BG = conf.get("WORKSPACES_BACKGROUND")

OBJS = f"""
* {{
    link-style: italic;
    link-hover-style: underline italic bold;
    link-hover-background: #fff 0%;
}}

MainScreen {{
    background: {BG};
    layout: vertical;
}}

HelpScreen {{
    layout: vertical;
    background: {BG};
    scrollbar-size: 1 1;
}}

DualSplit {{
    layout: grid;
    grid-size: 2;
    grid-columns: 2fr 8fr;
}}

Tree {{
     layers: L1 L2 L3 L4;
}}

WorkspaceTree, TodoTree, EmptyWidget {{
    background: {BG};
    border: {DIM};
    border-title-background: {BORDER_TITLE_DIM[1]};
    border-title-color: {BORDER_TITLE_DIM[0]};
    padding: 1;
    width: 100%;
    height: 100%;
    layer: L2;
}}

WorkspaceTree, WorkspaceTree > EmptyWidget {{
    background: {WORKSPACES_BG}
}}

TodoTree, TodoTree > EmptyWidget {{
    background: {TODOS_BG}
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
