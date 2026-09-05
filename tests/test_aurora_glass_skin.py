"""Registration contract for the Aurora Glass WebUI skin."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "static/index.html").read_text(encoding="utf-8")
BOOT = (ROOT / "static/boot.js").read_text(encoding="utf-8")
CONFIG = (ROOT / "api/config.py").read_text(encoding="utf-8")
CSS = (ROOT / "static/style.css").read_text(encoding="utf-8")


def test_aurora_glass_is_registered_at_all_four_webui_boundaries():
    assert "'aurora-glass':1" in INDEX
    assert "{name:'Aurora Glass', value:'aurora-glass'" in BOOT
    assert '"aurora-glass",' in CONFIG
    assert ':root[data-skin="aurora-glass"]{' in CSS
    assert ':root[data-skin="aurora-glass"]:not(.dark){' in CSS


def test_aurora_glass_respects_reduced_motion_and_has_opaque_fallback():
    assert "@media (prefers-reduced-motion:reduce)" in CSS
    assert ':root[data-skin="aurora-glass"] body::before,' in CSS
    assert "animation:none!important" in CSS
    assert "@supports not ((backdrop-filter:blur(1px))" in CSS
    assert "background:var(--glass-fallback)!important" in CSS
