import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "static/index.html").read_text(encoding="utf-8")
BOOT = (ROOT / "static/boot.js").read_text(encoding="utf-8")
CONFIG = (ROOT / "api/config.py").read_text(encoding="utf-8")
CSS = re.sub(r"\s+", "", (ROOT / "static/style.css").read_text(encoding="utf-8")).lower()


class ClaudeDesktopSkinTests(unittest.TestCase):
    def test_claude_skin_is_registered_end_to_end(self):
        self.assertRegex(INDEX, r"skins=\{[^}]*claude:1")
        self.assertIn("{name:'Claude Desktop', value:'claude'", BOOT)
        self.assertIn('"claude",', CONFIG)

    def test_claude_skin_has_warm_light_and_dark_tokens(self):
        self.assertIn(':root[data-skin="claude"]{', CSS)
        self.assertIn('--bg:#f7f6f2', CSS)
        self.assertIn('--sidebar:#eeece6', CSS)
        self.assertIn('--accent:#d97757', CSS)
        self.assertIn(':root.dark[data-skin="claude"]{', CSS)

    def test_claude_skin_matches_reference_geometry(self):
        self.assertIn(':root[data-skin="claude"].sidebar{width:272px', CSS)
        self.assertIn(':root[data-skin="claude"].messages-inner{max-width:800px', CSS)
        self.assertIn(':root[data-skin="claude"].composer-box{max-width:760px', CSS)
        self.assertIn(':root[data-skin="claude"].empty-stateh2{font-family:var(--font-display)', CSS)
        self.assertIn(':root[data-skin="claude"].suggestion-grid{flex-direction:row', CSS)

    def test_claude_skin_preserves_bidi_content_contract(self):
        claude_css = CSS.split('/*──skin:claudedesktop', 1)[1]
        self.assertNotIn('direction:rtl', claude_css)
        self.assertNotIn('direction:ltr', claude_css)
        self.assertNotIn('unicode-bidi', claude_css)


if __name__ == "__main__":
    unittest.main()
