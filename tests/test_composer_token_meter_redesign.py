import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = (ROOT / "static/ui.js").read_text(encoding="utf-8")
CSS = (ROOT / "static/style.css").read_text(encoding="utf-8")


def _indicator_body():
    start = UI.index("function _syncCtxIndicator")
    end = UI.index("// ── Touch support: toggle context tooltip on tap", start)
    return UI[start:end]


def _run_indicator(usage):
    body = _indicator_body()
    script = f"""
const nodes={{}};
for(const id of ['ctxIndicatorWrap','ctxIndicator','ctxRingValue','ctxPercent','ctxTooltipTitle','ctxTooltipUsage','ctxTooltipTokens','ctxTooltipThreshold','ctxTooltipCost','ctxTooltipCompress','ctxCompressBtn']){{
  nodes[id]={{style:{{}},classList:{{remove(){{}},toggle(){{}}}},removeAttribute(){{}},setAttribute(k,v){{this[k]=v;}}}};
}}
global.$=id=>nodes[id]||null;
global.window={{_composerControlVisibility:{{hide_composer_context:false}}}};
global._fmtTokens=n=>{{n=Number(n)||0;if(n>=1e6)return (n/1e6).toFixed(1).replace(/\\.0$/,'')+'M';if(n>=1e3)return (n/1e3).toFixed(1).replace(/\\.0$/,'')+'k';return String(n);}};
global.t=(key,...args)=>key+':'+args.join(',');
global._syncMobileCtxDisplay=()=>{{}};
global._setCtxCompressButton=()=>{{}};
{body}
_syncCtxIndicator({json.dumps(usage)});
console.log(JSON.stringify({{
 center:nodes.ctxPercent.textContent,
 dash:nodes.ctxRingValue.style.strokeDashoffset,
 label:nodes.ctxIndicator['aria-label'],
 title:nodes.ctxTooltipTitle.textContent,
 usage:nodes.ctxTooltipUsage.textContent,
 tokens:nodes.ctxTooltipTokens.textContent,
 threshold:nodes.ctxTooltipThreshold.textContent,
 cost:nodes.ctxTooltipCost.textContent,
 visible:nodes.ctxIndicatorWrap.style.display
}}));
"""
    out = subprocess.run(["node", "-e", script], cwd=ROOT, capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def test_circle_center_shows_current_context_tokens_not_percent():
    out = _run_indicator({
        "input_tokens": 120000,
        "output_tokens": 8000,
        "last_prompt_tokens": 98765,
        "context_length": 200000,
    })
    assert out["center"] == "98.8k"
    assert "49%" in out["label"]


def test_post_compression_estimate_wins_for_circle_and_ring():
    out = _run_indicator({
        "input_tokens": 300000,
        "output_tokens": 20000,
        "last_prompt_tokens": 170000,
        "post_compression_context_tokens_estimate": 42000,
        "context_length": 200000,
    })
    assert out["center"] == "42k"
    assert "21%" in out["label"]


def test_popup_reports_session_breakdown_capacity_and_remaining():
    out = _run_indicator({
        "input_tokens": 120000,
        "output_tokens": 8000,
        "last_prompt_tokens": 98765,
        "context_length": 200000,
        "cache_read_tokens": 90000,
        "cache_write_tokens": 1200,
        "cache_hit_percent": 75,
        "threshold_tokens": 150000,
        "estimated_cost": 0.123,
    })
    assert out["title"] == "مصرف توکن"
    assert "Context فعلی: 98.8k" in out["usage"]
    assert "ظرفیت: 200k" in out["usage"]
    assert "باقی‌مانده: 101.2k" in out["usage"]
    assert "ورودی: 120k" in out["tokens"]
    assert "خروجی: 8k" in out["tokens"]
    assert "مجموع: 128k" in out["tokens"]
    assert "Auto-compress: 150k" in out["threshold"]
    assert "Cache: 75%" in out["cost"]


def test_click_toggles_token_popup_instead_of_opening_advanced_panel():
    src = UI[UI.index("// ── Touch support: toggle context tooltip on tap"):UI.index("function _setMessageScrollToBottom")]
    assert "function toggleComposerTokenTooltip" in src
    assert "ctx-tooltip-active" in src
    assert "aria-hidden" in src
    assert "btn.addEventListener('click',toggleComposerTokenTooltip)" in src
    assert "btn.addEventListener('click',openComposerContextMenu)" not in src


def test_chatgpt_skin_exposes_and_sizes_token_meter():
    compact = "".join(CSS.split()).lower()
    assert ':root[data-skin="chatgpt"]#ctxindicatorwrap{display:inline-flex!important' in compact
    assert ':root[data-skin="chatgpt"].ctx-ring{width:34px;height:34px' in compact
    assert ':root[data-skin="chatgpt"].ctx-ring-svg{width:34px;height:34px' in compact
    assert ':root[data-skin="chatgpt"].ctx-ring-center{' in compact
    assert "font-size:8.5px" in compact
    assert "font-family:var(--font-mono)" in compact
