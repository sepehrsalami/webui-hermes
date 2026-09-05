import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "static/index.html").read_text(encoding="utf-8")
BOOT = (ROOT / "static/boot.js").read_text(encoding="utf-8")
CONFIG = (ROOT / "api/config.py").read_text(encoding="utf-8")
CSS_RAW = (ROOT / "static/style.css").read_text(encoding="utf-8")
CSS = re.sub(r"\s+", "", CSS_RAW).lower()


class ChatGPTPersianSkinTests(unittest.TestCase):
    def test_skin_is_registered_end_to_end(self):
        self.assertRegex(INDEX, r"skins=\{[^}]*chatgpt:1")
        self.assertIn("{name:'ChatGPT Persian', value:'chatgpt'", BOOT)
        self.assertIn('"chatgpt",', CONFIG)

    def test_skin_uses_reference_palette_and_geometry(self):
        self.assertIn(':root[data-skin="chatgpt"]{', CSS)
        self.assertIn('--bg:#fff', CSS)
        self.assertIn('--sidebar:#fcfcfc', CSS)
        self.assertIn('--text:#0d0d0d', CSS)
        self.assertIn('--muted:#5d5d5d', CSS)
        self.assertIn(':root[data-skin="chatgpt"].composer-box{max-width:768px', CSS)
        self.assertIn('border-radius:28px', CSS)
        self.assertIn(':root[data-skin="chatgpt"].messages-inner{max-width:768px', CSS)

    def test_local_vazirmatn_faces_are_declared(self):
        for weight, filename in (
            (300, "Vazirmatn-Light.woff2"),
            (400, "Vazirmatn-Regular.woff2"),
            (500, "Vazirmatn-Medium.woff2"),
            (700, "Vazirmatn-Bold.woff2"),
        ):
            self.assertIn("@font-face", CSS_RAW)
            self.assertIn(filename, CSS_RAW)
            self.assertRegex(CSS_RAW, rf"font-weight:\s*{weight}")

    def test_persian_scale_is_explicit_and_readable(self):
        self.assertIn('--font-persian:"vazirmatn"', CSS)
        self.assertIn('--font-ui:var(--font-persian)', CSS)
        self.assertIn('--font-conversation:var(--font-persian)', CSS)
        self.assertIn('--message-body-font-size:16px', CSS)
        self.assertIn('--message-body-line-height:1.9', CSS)
        self.assertIn(':root[data-skin="chatgpt"]textarea#msg{font-family:var(--font-persian)', CSS)

    def test_skin_does_not_override_shared_message_bidi_contract(self):
        block = CSS.split('/*──skin:chatgptpersian', 1)[1]
        self.assertNotIn('.msg-body', block)
        # The Persian composer placeholder may be explicitly RTL; message prose
        # must still remain owned by the shared bidi layer.
        self.assertNotIn('.msg-body{direction:rtl', block)
        # Technical model identifiers may be explicitly isolated LTR; message
        # bodies and prose direction remain owned by the shared bidi layer.
        self.assertNotIn('.msg-body{direction:ltr', block)
        self.assertNotIn('.msg-body{unicode-bidi', block)


if __name__ == "__main__":
    unittest.main()
