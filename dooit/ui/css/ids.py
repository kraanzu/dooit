"""
CSS File for propery `id`
"""

from . import conf

DIM = conf.get("BORDER_DIM")
LIT = conf.get("BORDER_LIT")

ids = f"""
#dim {{
    border: {DIM} heavy;
}}

#dim {{
    border: {LIT} heavy;
}}
"""
