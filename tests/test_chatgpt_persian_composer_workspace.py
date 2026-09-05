import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "static/index.html").read_text(encoding="utf-8")
PANELS = (ROOT / "static/panels.js").read_text(encoding="utf-8")
CSS = re.sub(r"\s+", "", (ROOT / "static/style.css").read_text(encoding="utf-8")).lower()


def test_composer_uses_requested_persian_placeholder_and_keeps_auto_direction():
    assert '<textarea id="msg" dir="auto" rows="1" placeholder="چه کمکی از دستم برمی‌آید؟"></textarea>' in INDEX


def test_chatgpt_workspace_manage_action_is_persian_at_render_source():
    assert "const _chatGptPersianWorkspace=" in PANELS
    assert "'مدیریت فضاهای کاری'" in PANELS
    assert "'باز کردن پنل فضاهای کاری'" in PANELS


def test_chatgpt_placeholder_is_right_aligned_without_forcing_typed_english_rtl():
    assert ':root[data-skin="chatgpt"]textarea#msg::placeholder{' in CSS
    assert 'text-align:right' in CSS
    block = CSS.split(':root[data-skin="chatgpt"]textarea#msg::placeholder{', 1)[1].split('}', 1)[0]
    assert 'direction:rtl' in block
    assert ':root[data-skin="chatgpt"]textarea#msg:dir(ltr){text-align:left' in CSS
    assert ':root[data-skin="chatgpt"]textarea#msg:dir(rtl){text-align:right' in CSS


def test_chatgpt_workspace_split_control_has_one_shell_and_clear_actions():
    assert ':root[data-skin="chatgpt"].composer-workspace-group{' in CSS
    assert 'isolation:isolate' in CSS
    assert ':root[data-skin="chatgpt"].composer-workspace-files-btn{' in CSS
    assert ':root[data-skin="chatgpt"].composer-workspace-chip{' in CSS
    assert 'border-inline-start:1pxsolidvar(--border)' in CSS
    assert 'unicode-bidi:isolate' in CSS
