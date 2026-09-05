from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = (ROOT / "static/ui.js").read_text(encoding="utf-8")
CSS = (ROOT / "static/style.css").read_text(encoding="utf-8")


def test_turn_usage_has_one_shared_builder():
    assert "function _buildTurnUsageModule(" in UI
    start = UI.index("function _buildTurnUsageModule(")
    end = UI.index("function ", start + 20)
    body = UI[start:end]
    assert "turn-usage-module" in body
    assert "turn-usage-summary" in body
    assert "turn-usage-details" in body
    assert "turn-usage-chip" in body


def test_turn_usage_summary_contains_input_output_total_and_cache():
    start = UI.index("function _buildTurnUsageModule(")
    end = UI.index("function ", start + 20)
    body = UI[start:end]
    for token in ("input_tokens", "output_tokens", "cache_hit_percent", "turn-usage-total"):
        assert token in body
    assert "ورودی" in body
    assert "خروجی" in body
    assert "مجموع" in body
    assert "کش" in body


def test_turn_usage_details_include_cache_cost_duration_and_ttft_when_available():
    start = UI.index("function _buildTurnUsageModule(")
    end = UI.index("function ", start + 20)
    body = UI[start:end]
    for field in ("cache_read_tokens", "cache_write_tokens", "estimated_cost", "_turnDuration", "_firstTokenMs"):
        assert field in body
    assert '<bdi dir="ltr">' in body


def test_turn_usage_omits_empty_module_and_zero_detail_rows():
    start = UI.index("function _buildTurnUsageModule(")
    end = UI.index("function ", start + 20)
    body = UI[start:end]
    assert "if(!hasUsage)returnnull" in body.replace(" ", "")
    assert "if(cacheRead>0)" in body
    assert "if(cacheWrite>0)" in body
    assert "if(cost>0)" in body


def test_assistant_footer_uses_new_module_instead_of_plain_usage_span():
    assert "const usage=_buildTurnUsageModule(msg);" in UI
    assert "usage.className='msg-usage-inline'" not in UI


def test_usage_module_is_visible_without_hover_and_responsive():
    compact = "".join(CSS.split()).lower()
    assert ".turn-usage-module{" in compact
    assert ".msg-foot:has(.turn-usage-module){opacity:1" in compact
    assert ".turn-usage-summary{" in compact
    assert "flex-wrap:wrap" in compact
    assert ".turn-usage-modulebdi{direction:ltr" in compact
    assert "@media(max-width:640px)" in compact
