"""
CSS file for property `class`
"""

from . import conf

LIT = conf.get("BORDER_LIT")
BORDER_TITLE_LIT = conf.get("BORDER_TITLE_LIT")
YANK = conf.get("YANK_COLOR")

classes = f"""
.dim {{
    opacity: 70%;
}}

.highlight {{
    text-style: bold;
}}

.editing{{
    text-style: bold;
}}

.focus {{
    border: {LIT};
    border-title-background: {LIT};
    border-title-color: {BORDER_TITLE_LIT};
}}

.no-border {{
    border: none;
}}

.sort-hide, .search-hide {{
    display: none;
}}

.hide {{
    display: none;
}}

.padding {{
    padding-right: 1;
}}

.dock-left {{
    dock: left;
}}

.dock-right {{
    dock: right;
}}

.current {{
    layer: L3;
}}

.yank {{
    background: {YANK};
}}
"""
