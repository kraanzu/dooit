"""
CSS File for python classes
"""


OBJS = f"""
* {{
    link-style: italic;
    link-style-hover: underline italic bold;
    link-background-hover: #fff 0%;
}}

MainScreen {{
    layout: vertical;
}}

HelpScreen {{
    layout: vertical;
    scrollbar-size: 1 1;
}}

DualSplit {{
    layout: grid;
    grid-size: 2 1;
    grid-columns: 2fr 8fr;
}}

Tree {{
     layers: L1 L2 L3 L4;
}}

WorkspaceTree, TodoTree, EmptyWidget {{
    padding: 1;
    width: 100%;
    height: 100%;
    layer: L2;
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
