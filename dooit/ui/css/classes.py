"""
CSS file for property `class`
"""

from . import conf

DIM = conf.get("BORDER_DIM")
LIT = conf.get("BORDER_LIT")

classes = f"""
.dim {{
    border: {DIM} heavy;
}}

.dim {{
    border: {LIT} heavy;
}}
"""
