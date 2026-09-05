from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = (ROOT / "static/ui.js").read_text(encoding="utf-8")
CSS = (ROOT / "static/style.css").read_text(encoding="utf-8")


def _copy_body() -> str:
    start = UI.index("function addCopyButtons(")
    end = UI.index("let _mermaidLoading", start)
    return UI[start:end]


def test_shell_fences_are_recognized_in_shared_post_processor():
    body = _copy_body()
    assert "language-bash" in body
    assert "language-shell" in body
    assert "language-zsh" in body
    assert "language-sh" in body
    assert "shell-code-header" in body
    assert "shell-code-pre" in body


def test_shell_header_is_rebuilt_with_copy_left_and_language_right():
    body = _copy_body()
    assert "shell-code-copy" in body
    assert "shell-code-meta" in body
    assert "shell-code-language" in body
    assert "shell-code-glyph" in body
    assert "Bash" in body
    assert "aria-label" in body


def test_shell_block_has_reference_geometry_and_typography():
    compact = "".join(CSS.split()).lower()
    assert ".shell-code-header{" in compact
    assert "justify-content:space-between" in compact
    assert "border-radius:28px28px00" in compact
    assert ".shell-code-pre{" in compact
    assert "border-radius:0028px28px" in compact
    assert "background:var(--code-bg)!important" in compact
    assert "color:var(--pre-text)!important" in compact
    assert "border:1pxsolidvar(--border)!important" in compact
    assert "font-family:var(--font-mono)" in compact
    assert "line-height:1.6" in compact


def test_shell_syntax_palette_covers_strings_variables_options_and_numbers():
    compact = "".join(CSS.split()).lower()
    for selector in (
        ".shell-code-pre.token.string",
        ".shell-code-pre.token.variable",
        ".shell-code-pre.token.parameter",
        ".shell-code-pre.token.number",
    ):
        assert selector in compact


def test_shell_code_remains_ltr_and_horizontally_scrollable():
    compact = "".join(CSS.split()).lower()
    block = compact.split(".shell-code-pre{", 1)[1].split("}", 1)[0]
    assert "direction:ltr" in block
    assert "unicode-bidi:isolate" in block
    assert "overflow-x:auto" in block
