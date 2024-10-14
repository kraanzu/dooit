from ..theme import DooitThemeBase


class Gruvbox(DooitThemeBase):
    _name = "dooit-gruvbox"

    background_1: str = "#282828"  # Darkest
    background_2: str = "#3c3836"  # Lighter
    background_3: str = "#504945"  # Lightest

    # foreground colors
    foreground_1: str = "#7c6f64"  # Darkest
    foreground_2: str = "#ebdbb2"  # Lighter
    foreground_3: str = "#fbf1c7"  # Lightest

    # other colors
    red: str = "#fb4934"
    orange: str = "#fe8019"
    yellow: str = "#fabd2f"
    green: str = "#b8bb26"
    blue: str = "#83a598"
    purple: str = "#d3869b"
    magenta: str = "#d3869b"
    cyan: str = "#8ec07c"

    # accent colors
    primary: str = yellow
    secondary: str = green
