from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = (ROOT / "static/ui.js").read_text(encoding="utf-8")
CSS = (ROOT / "static/style.css").read_text(encoding="utf-8")
INDEX = (ROOT / "static/index.html").read_text(encoding="utf-8")


def _function(name: str, next_name: str) -> str:
    start = UI.index(name)
    end = UI.index(next_name, start)
    return UI[start:end]


def test_chatgpt_model_picker_uses_trigger_anchored_floating_positioning():
    body = _function("function _positionModelDropdown()", "function _readModelOverflowData")
    assert "document.documentElement.dataset.skin==='chatgpt'" in body
    assert "if(isPhone||isChatGptSkin)" in body
    assert "document.body.appendChild(dd)" in body
    assert "Math.min(360" in body
    assert "anchorRect.width" in body
    assert "viewportRight-menuWidth-margin" in body


def test_model_rows_have_selected_check_and_ltr_isolated_identifier():
    body = _function("function renderModelDropdown()", "async function selectModelFromDropdown")
    assert 'class="model-opt-check"' in body
    assert '<bdi class="model-opt-id" dir="ltr">' in body
    assert "_modelPickerBadgeLabel" in body
    assert "_modelPickerTechnicalLabel" in body


def test_chatgpt_picker_localizes_primary_and_deduplicates_custom_id():
    assert "function _modelPickerBadgeLabel(" in UI
    assert "'مدل اصلی'" in UI
    assert "function _modelPickerTechnicalLabel(" in UI
    assert "@custom:" in UI


def test_chatgpt_picker_has_compact_connected_visual_contract():
    compact = ''.join(CSS.split())
    assert ':root[data-skin="chatgpt"].model-dropdown.model-dropdown--floating' in compact
    assert 'border-radius:16px' in compact
    assert ':root[data-skin="chatgpt"].model-opt-check' in compact
    assert ':root[data-skin="chatgpt"].model-opt-id{direction:ltr' in compact


def test_context_zero_control_has_explicit_accessible_label():
    assert 'aria-label="Context usage: 0 percent"' in INDEX
