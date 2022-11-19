"""
Main CSS File for App
"""

from dooit.utils.default_config import BACKGROUND


screen_CSS = f"""
Screen {{
    background: {BACKGROUND};
    layout: grid;
    grid-size: 2 2;
    grid-columns: 2fr 8fr;
    grid-rows: 1fr 1;
}}

StatusBar {{
    column-span: 2;
}}

Vertical {{
    column-span: 2;
    row-span: 2;
    scrollbar-size: 1 1;
}}
"""
