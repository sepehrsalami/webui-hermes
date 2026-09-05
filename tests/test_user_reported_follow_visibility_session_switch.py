"""Regression contracts for the 2026-08-21 live WebUI report."""

from pathlib import Path

ROOT = Path(__file__).parents[1]
ROUTES = (ROOT / "api" / "routes.py").read_text(encoding="utf-8")
SESSIONS = (ROOT / "static" / "sessions.js").read_text(encoding="utf-8")
MESSAGES = (ROOT / "static" / "messages.js").read_text(encoding="utf-8")


def _function_body(source: str, signature: str, next_marker: str) -> str:
    start = source.index(signature)
    end = source.index(next_marker, start)
    return source[start:end]


def test_raw_all_marks_native_webui_rows_actionable():
    body = _function_body(
        ROUTES,
        "def _raw_all_session_sidebar_payload",
        "def _hidden_archived_sidebar_reference_sessions",
    )
    assert 'read_only = source != "webui"' in body


def test_session_switch_bounds_draft_network_wait_before_loading_target():
    body = _function_body(SESSIONS, "async function loadSession(sid)", "// ── Handoff hint logic")
    assert "await _saveComposerDraftNow(currentSid" in body
    save = _function_body(SESSIONS, "function _saveComposerDraftNow", "// Restore composer draft")
    assert "Promise.race" in save
    assert "_DRAFT_SWITCH_WAIT_MS" in save


def test_live_token_render_keeps_following_when_reader_has_not_scrolled():
    body = _function_body(MESSAGES, "function _scheduleRender", "function _completeAutomaticCompressionOnLiveProgress")
    assert "_followFreshStreamTailIfOwned();" in body
    helper = _function_body(
        MESSAGES,
        "function _followFreshStreamTailIfOwned",
        "function _completeAutomaticCompressionOnLiveProgress",
    )
    assert "_streamScrollInputGenerationAtAttach" in helper
    assert "_messageScrollInputGenerationValue()" in helper
    assert "scrollToBottom" in helper
