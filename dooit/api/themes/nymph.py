from ..theme import DooitThemeBase


class Nymph(DooitThemeBase):
    background_1: str = "#1A2023"  # Darkest
    background_2: str = "#252B2E"  # Lighter
    background_3: str = "#373D40"  # Lightest

    # foreground colors
    foreground_1: str = "#5B6265"  # Darkest
    foreground_2: str = "#BCC4C9"  # Lighter
    foreground_3: str = "#ECEFF4"  # Lightest

    # other colors
    red: str = "#BC7171"
    orange: str = "#C99577"
    yellow: str = "#D5BE82"
    green: str = "#9FBC85"
    blue: str = "#7C9BB4"
    magenta: str = "#A883A2"
    cyan: str = "#89B7B0"

    # accent colors
    primary: str = cyan
    secondary: str = blue
