from pathlib import Path
from platformdirs import user_cache_dir
from dooit.api.theme import DooitThemeBase
from uuid import uuid4

dooit_cache_path = Path(user_cache_dir("dooit"))


def generate_random_id():
    return uuid4().hex


class CssManager:
    base_css: Path = Path(__file__).parent.parent.parent / "ui" / "styles.tcss"
    stylesheets: Path = dooit_cache_path / "stylesheets"

    css_file: Path = dooit_cache_path / "dooit.tcss"
    theme_css_file: Path = dooit_cache_path / "theme.tcss"
    base_css_file: Path = dooit_cache_path / "base.tcss"

    def _create_files(self):
        if not self.stylesheets.exists():
            self.stylesheets.mkdir(
                parents=True,
                exist_ok=True,
            )

        if not self.theme_css_file.exists():
            self.theme_css_file.touch()

        if not self.base_css_file.exists():
            self.base_css_file.touch()

    def refresh_css(self):
        self._create_files()

        css = ""

        # setup theme variables
        with open(self.theme_css_file, "r") as f:
            css = css + "\n" + f.read()

        # setup base variables
        with open(self.base_css_file, "r") as f:
            css = css + "\n" + f.read()

        # inject extra stylesheets
        for sheet in self.stylesheets.iterdir():
            with open(sheet, "r") as f:
                css = css + "\n" + f.read()

        self.write(css)

    def set_theme(self, theme: DooitThemeBase):
        with open(self.theme_css_file, "w") as f:
            f.write(theme.to_css())

        self.refresh_css()

    def inject_css(self, css: str) -> str:
        uuid = generate_random_id()
        css_file = self.stylesheets / f"{uuid}.tcss"

        with open(css_file, "w") as f:
            f.write(css)

        self.refresh_css()
        return uuid

    def uninject_css(self, _id: str) -> bool:
        css_file = self.stylesheets / f"{_id}.tcss"

        if not css_file.exists():
            return False

        css_file.unlink()
        self.refresh_css()
        return True

    def write(self, css: str):
        with open(self.css_file, "w") as f:
            f.write(css)
