from textual.widget import Widget
from dooit.utils.conf_reader import config_man

BG = config_man.get("BAR_BACKGROUND")


class AutoHorizontal(Widget):
    DEFAULT_CSS = """
    AutoHorizontal {
        layout: horizontal;
        max-height: 1;
        width: auto;
    }
    """


class StatusMiddle(Widget):
    DEFAULT_CSS = f"""
    StatusMiddle {{
        background: {BG};
        padding: 0 1 0 1;
    }}
    """
