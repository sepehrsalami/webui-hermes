"""Accessibility contracts for the compact/mobile sidebar navigation."""

from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "static/index.html").read_text(encoding="utf-8")


class _SidebarNavButtonParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_sidebar_nav = False
        self.depth = 0
        self.buttons: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "div" and "sidebar-nav" in values.get("class", "").split():
            self.in_sidebar_nav = True
            self.depth = 1
            return
        if not self.in_sidebar_nav:
            return
        if tag == "div":
            self.depth += 1
        if tag == "button" and "nav-tab" in values.get("class", "").split():
            self.buttons.append(values)

    def handle_endtag(self, tag: str) -> None:
        if self.in_sidebar_nav and tag == "div":
            self.depth -= 1
            if self.depth == 0:
                self.in_sidebar_nav = False


def test_every_sidebar_navigation_button_has_a_localizable_accessible_name():
    parser = _SidebarNavButtonParser()
    parser.feed(INDEX)

    assert parser.buttons, "sidebar navigation buttons were not discovered"
    unnamed = [
        button.get("data-panel") or button.get("id") or "unknown"
        for button in parser.buttons
        if not button.get("aria-label") or not button.get("data-i18n-aria-label")
    ]
    assert not unnamed, f"sidebar navigation buttons lack accessible names: {unnamed}"
