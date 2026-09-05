import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS_RAW = (ROOT / "static/style.css").read_text(encoding="utf-8")
CSS = re.sub(r"\s+", "", CSS_RAW).lower()


def _chatgpt_block() -> str:
    return CSS.split("/*──skin:chatgptpersian", 1)[1]


def test_chatgpt_skin_hides_session_source_and_project_filter_bars():
    block = _chatgpt_block()
    assert ':root[data-skin="chatgpt"].session-source-tabs{display:none!important;}' in block
    assert ':root[data-skin="chatgpt"].project-bar{display:none!important;}' in block


def test_chatgpt_composer_controls_share_one_height_and_radius_system():
    block = _chatgpt_block()
    assert '--composer-control-size:32px' in block
    assert '--composer-control-radius:999px' in block
    assert ':root[data-skin="chatgpt"].composer-footer{gap:8px' in block
    assert ':root[data-skin="chatgpt"].composer-left' in block
    assert ':root[data-skin="chatgpt"].composer-right' in block


def test_chatgpt_icon_profile_workspace_model_and_send_controls_are_aligned():
    block = _chatgpt_block()
    for selector in (
        '.icon-btn',
        '.composer-profile-chip',
        '.composer-workspace-group',
        '.composer-model-chip',
        '.ctx-indicator',
        '.send-btn',
    ):
        assert f':root[data-skin="chatgpt"]{selector}' in block
    assert 'height:var(--composer-control-size)' in block
    assert 'min-height:var(--composer-control-size)' in block
    assert 'border-radius:var(--composer-control-radius)' in block


def test_chatgpt_composer_dividers_are_hidden_to_reduce_visual_noise():
    assert ':root[data-skin="chatgpt"].composer-divider{display:none;}' in _chatgpt_block()
