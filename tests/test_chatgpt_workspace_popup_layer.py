from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PANELS = (ROOT / "static/panels.js").read_text(encoding="utf-8")
CSS = (ROOT / "static/style.css").read_text(encoding="utf-8")


def _block(start: str, end: str) -> str:
    a = PANELS.index(start)
    b = PANELS.index(end, a)
    return PANELS[a:b]


def test_composer_workspace_popup_is_reparented_outside_composer():
    body = _block("function _positionComposerWsDropdown()", "function _positionProfileDropdown()")
    assert "document.body.appendChild(dd)" in body
    assert "ws-dropdown--floating" in body
    assert "position:fixed" not in body  # positioning belongs to CSS class
    assert "getBoundingClientRect()" in body
    assert "viewportRight-menuWidth-margin" in body


def test_workspace_popup_restores_original_dom_slot_on_close():
    assert "let _composerWsDropdownHome=null" in PANELS
    assert "function _restoreComposerWsDropdownHome(" in PANELS
    close = _block("function closeWsDropdown()", "document.addEventListener('click'")
    assert "_restoreComposerWsDropdownHome()" in close


def test_workspace_popup_layer_escapes_overflow_and_stacking_contexts():
    compact = "".join(CSS.split()).lower()
    assert ".ws-dropdown.ws-dropdown--floating{" in compact
    floating = compact.split(".ws-dropdown.ws-dropdown--floating{", 1)[1].split("}", 1)[0]
    assert "position:fixed" in floating
    assert "z-index:9999" in floating
    assert "overflow-y:auto" in floating


def test_chatgpt_composer_remains_below_floating_popup():
    compact = "".join(CSS.split()).lower()
    assert ':root[data-skin="chatgpt"].composer-box{' in compact
    assert "z-index:1" in compact.split(':root[data-skin="chatgpt"].composer-box{', 1)[1].split("}", 1)[0]
