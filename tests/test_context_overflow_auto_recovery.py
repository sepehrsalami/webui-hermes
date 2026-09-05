"""Regression coverage for automatic WebUI context-overflow recovery."""

from pathlib import Path

from api import streaming


ROOT = Path(__file__).resolve().parents[1]
MESSAGES_JS = (ROOT / "static" / "messages.js").read_text(encoding="utf-8")


def test_exact_provider_context_window_error_is_recoverable_overflow():
    message = "[Error] Your input exceeds the context window of this model. Please adjust your input and try again."

    classified = streaming._classify_provider_error(message, Exception(message))

    assert classified["type"] == "context_overflow"
    assert classified["retryable"] is True


def test_compression_exhausted_remains_terminal_continuation_case():
    message = "Context length exceeded and cannot compress further: compression_exhausted"

    classified = streaming._classify_provider_error(message, Exception(message))

    assert classified["type"] == "compression_exhausted"
    assert classified.get("retryable") is not True


def test_browser_context_recovery_is_bounded_and_preserves_pending_prompt():
    assert "async function _recoverContextOverflowOnce(" in MESSAGES_JS
    assert "context-overflow-retry:" in MESSAGES_JS
    assert "sessionStorage.getItem(retryKey)" in MESSAGES_JS
    assert "sessionStorage.setItem(retryKey,'1')" in MESSAGES_JS
    assert "sessionStorage.removeItem(retryKey)" in MESSAGES_JS
    assert "_lastUserPromptForContextRecovery" in MESSAGES_JS
    assert "/api/session/compress/start" in MESSAGES_JS
    assert "cmdRetry" in MESSAGES_JS


def test_apperror_routes_only_context_overflow_to_automatic_recovery():
    assert "d.type==='context_overflow'" in MESSAGES_JS
    assert "_recoverContextOverflowOnce" in MESSAGES_JS
