class DooitThemeBase:
    # background colors
    background_1: str  # Darkest
    background_2: str  # Lighter
    background_3: str  # Lightest

    # foreground colors
    foreground_1: str  # Darkest
    foreground_2: str  # Lighter
    foreground_3: str  # Lightest

    # other colors
    red: str
    orange: str
    yellow: str
    green: str
    blue: str
    purple: str
    pink: str
    gray: str

    # accent colors
    primary: str
    secondary: str

    def to_css(self) -> str:
        css = f"""
        $background_1: {self.background_1};
        $background_2: {self.background_2};
        $background_3: {self.background_3};

        $foreground_1: {self.foreground_1};
        $foreground_2: {self.foreground_2};
        $foreground_3: {self.foreground_3};

        $red: {self.red};
        $orange: {self.orange};
        $yellow: {self.yellow};
        $green: {self.green};
        $blue: {self.blue};
        $purple: {self.purple};
        $pink: {self.pink};
        $gray: {self.gray};

        $primary: {self.primary};
        $secondary: {self.secondary};
        """

        return css