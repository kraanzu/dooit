"""
CSS file for property `class`
"""

from . import conf

LIT = conf.get("BORDER_LIT")
BORDER_TITLE_LIT = conf.get("BORDER_TITLE_LIT")
if not isinstance(BORDER_TITLE_LIT, tuple):
    BORDER_TITLE_LIT = BORDER_TITLE_LIT, LIT
YANK = conf.get("YANK_COLOR")

classes = f"""
.highlight {{
    background: #fff 10%;
}}

.focus {{
    border: {LIT};
    border-title-background: {BORDER_TITLE_LIT[1]};
    border-title-color: {BORDER_TITLE_LIT[0]};
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
