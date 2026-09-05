from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = (ROOT / "static/ui.js").read_text(encoding="utf-8")
CSS = (ROOT / "static/style.css").read_text(encoding="utf-8")


def _copy_body() -> str:
    start = UI.index("function _referenceCodeLanguageLabel(")
    end = UI.index("let _mermaidLoading", start)
    return UI[start:end]


def test_all_ordinary_multiline_code_blocks_get_reference_classes():
    body = _copy_body()
    assert "reference-code-header" in body
    assert "reference-code-pre" in body
    assert "reference-code-copy" in body
    assert "reference-code-meta" in body
    assert "reference-code-language" in body
    assert "reference-code-glyph" in body


def test_unlabelled_fenced_block_gets_text_header():
    body = _copy_body()
    assert "document.createElement('div')" in body
    assert "pre.parentNode.insertBefore(effectiveHeader,pre)" in body
    assert "Text" in body


def test_language_labels_are_human_readable():
    body = _copy_body()
    for label in ("Bash", "Shell", "JSON", "Python", "JavaScript", "TypeScript", "HTML", "CSS", "YAML", "Text"):
        assert label in body


def test_specialized_operational_blocks_are_excluded():
    body = _copy_body()
    for selector in ("diff-block", "provider-error-details", "tool-card-result", "process-wakeup"):
        assert selector in body
    assert "if(isSpecialized)return" in body.replace(" ", "")


def test_reference_frame_geometry_applies_to_every_language():
    compact = "".join(CSS.split()).lower()
    assert ".reference-code-header{" in compact
    assert "justify-content:space-between" in compact
    assert "border-radius:28px28px00" in compact
    assert ".reference-code-pre{" in compact
    assert "background:var(--code-bg)!important" in compact
    assert "color:var(--pre-text)!important" in compact
    assert "border:1pxsolidvar(--border)!important" in compact
    assert "border-radius:0028px28px" in compact


def test_reference_header_and_body_cannot_be_split_by_skin_child_margins():
    compact = "".join(CSS.split()).lower()
    header = compact.split(".reference-code-header{", 1)[1].split("}", 1)[0]
    pre = compact.split(".reference-code-pre{", 1)[1].split("}", 1)[0]
    assert "margin:14px00!important" in header
    assert "margin:0014px!important" in pre
    assert "border-bottom:0!important" in header
    assert "border-top:0!important" in pre


def test_reference_content_preserves_ltr_whitespace_and_scroll():
    compact = "".join(CSS.split()).lower()
    block = compact.split(".reference-code-pre{", 1)[1].split("}", 1)[0]
    assert "direction:ltr" in block
    assert "unicode-bidi:isolate" in block
    assert "overflow-x:auto!important" in block
    assert "white-space:pre!important" in block


def test_reference_syntax_palette_is_language_agnostic():
    compact = "".join(CSS.split()).lower()
    for selector in (
        ".reference-code-pre.token.string",
        ".reference-code-pre.token.variable",
        ".reference-code-pre.token.parameter",
        ".reference-code-pre.token.number",
        ".reference-code-pre.token.keyword",
        ".reference-code-pre.token.comment",
    ):
        assert selector in compact


def test_reference_frame_has_no_light_only_fixed_colors():
    compact = "".join(CSS.split()).lower()
    start = compact.index(".reference-code-header{")
    end = compact.index("/*backward-compatibleshellmarkers", start)
    block = compact[start:end]
    for fixed_color in ("#f7f7f7", "#191919", "#efefef", "#e8e8e8"):
        assert fixed_color not in block


def test_reference_frame_has_mobile_geometry():
    compact = "".join(CSS.split()).lower()
    assert "@media(max-width:700px)" in compact
    assert ".reference-code-header{min-height:46px" in compact
    assert ".reference-code-precode" in compact
