from ..theme import DooitThemeBase


class Nord(DooitThemeBase):
    background_1: str = "#2E3440"  # Darkest
    background_2: str = "#3B4252"  # Lighter
    background_3: str = "#434C5E"  # Lightest

    # foreground colors
    foreground_1: str = "#D8DEE9"  # Darkest
    foreground_2: str = "#E5E9F0"  # Lighter
    foreground_3: str = "#ECEFF4"  # Lightest

    # other colors
    red: str = "#BF616A"
    orange: str = "#D08770"
    yellow: str = "#EBCB8B"
    green: str = "#A3BE8C"
    blue: str = "#81a1c1"
    purple: str = "#B48EAD"
    magenta: str = "#B48EAD"
    cyan: str = "#8fbcbb"

    # accent colors
    primary: str = cyan
    secondary: str = blue
