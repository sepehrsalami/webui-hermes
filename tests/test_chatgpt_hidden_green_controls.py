import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = re.sub(r"\s+", "", (ROOT / "static/style.css").read_text(encoding="utf-8")).lower()


def test_chatgpt_skin_hides_green_marked_composer_controls():
    # Mic and focus-composer controls stay hidden in the ChatGPT skin.
    for selector in ("#btnmic", "#focuscomposercontrolsbtn"):
        assert f':root[data-skin="chatgpt"]{selector}' in CSS
        assert f':root[data-skin="chatgpt"]{selector}{{display:none!important;}}' in CSS


def test_chatgpt_skin_keeps_context_token_meter_visible():
    # Deliberate product change (2026-08-15 session): the context ring became
    # the Persian "مصرف توکن" token meter; the skin must NOT hide it.
    assert ':root[data-skin="chatgpt"]#ctxindicatorwrap{display:inline-flex!important;}' in CSS


def test_send_button_remains_visible_in_chatgpt_skin():
    block = CSS.split('/*──skin:chatgptpersian', 1)[1]
    assert '#btnsend{display:none' not in block
    assert '.send-btn{display:none' not in block
