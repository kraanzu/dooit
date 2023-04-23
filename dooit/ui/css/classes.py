"""
CSS file for property `class`
"""

from . import conf

LIT = conf.get("BORDER_LIT")

classes = f"""
.focus {{
    border: {LIT} heavy;
}}
"""
