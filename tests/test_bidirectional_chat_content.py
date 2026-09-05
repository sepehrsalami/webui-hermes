"""Regression contracts for mixed Persian/English chat rendering.

Active architecture (2026-08): Persian mode is an explicit user toggle,
the ``chat-content-rtl`` class on <html> (Settings → Preferences). Message
bodies always carry dir="auto"; the toggle scopes direction, list geometry,
and LTR isolation for code/math/diffs/tool output. The legacy
``prp-rtl-active`` static hook was removed with the upstream redesign.
"""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = (ROOT / "static" / "index.html").read_text(encoding="utf-8")
UI_JS = (ROOT / "static" / "ui.js").read_text(encoding="utf-8")
MESSAGES_JS = (ROOT / "static" / "messages.js").read_text(encoding="utf-8")
BOOT_JS = (ROOT / "static" / "boot.js").read_text(encoding="utf-8")
CSS = (ROOT / "static" / "style.css").read_text(encoding="utf-8")
I18N_FA = (ROOT / "static" / "i18n-fa.js").read_text(encoding="utf-8")


class BidirectionalChatContentTests(unittest.TestCase):
    def test_composer_base_is_automatic_and_toggle_forces_rtl_scoped(self):
        self.assertIn('<textarea id="msg" dir="auto"', INDEX_HTML)
        self.assertIn(".chat-content-rtl #msg{", CSS)
        self.assertIn("unicode-bidi:plaintext", CSS)

    def test_settled_and_live_message_bodies_use_automatic_direction(self):
        self.assertIn("body.className='msg-body';body.setAttribute('dir','auto');", MESSAGES_JS)
        self.assertIn("body.className = 'msg-body';\n    body.setAttribute('dir', 'auto');", UI_JS)
        self.assertIn('<div class="msg-body" dir="auto">', UI_JS)
        self.assertIn("body.className='msg-body';body.setAttribute('dir','auto');", BOOT_JS)

    def test_rtl_toggle_scopes_lists_and_ltr_token_isolation(self):
        self.assertIn(".chat-content-rtl .msg-body :is(ul,ol){", CSS)
        self.assertIn("padding-inline-start:", CSS)
        self.assertIn("unicode-bidi:isolate", CSS)
        self.assertIn(".chat-content-rtl .msg-body pre,", CSS)
        self.assertIn(".chat-content-rtl .msg-body code,", CSS)

    def test_direction_rules_do_not_force_english_messages_rtl(self):
        # Bare (unscoped) message rows/bodies must never hard-code RTL;
        # direction only applies under the opt-in chat-content-rtl class.
        self.assertIsNone(re.search(r"(?m)^\.msg-(?:row|body)\s*\{[^}]*direction:\s*rtl", CSS))
        self.assertIn(".chat-content-rtl .msg-row{", CSS)

    def test_persian_fonts_are_bundled_without_stale_global_hook(self):
        self.assertNotIn("prp-rtl-active", INDEX_HTML)
        self.assertIn('font-family:"Vazirmatn"', CSS)
        for weight in ("Light", "Regular", "Medium", "Bold"):
            font = ROOT / "static" / "fonts" / "persian-right-pro" / f"Vazirmatn-{weight}.woff2"
            self.assertTrue(font.is_file(), f"missing bundled font: {font.name}")

    def test_toggle_keeps_code_ltr_and_moves_list_markers_inline_start(self):
        self.assertIn(".chat-content-rtl .msg-body pre *{", CSS)
        self.assertIn("margin-inline:0!important", CSS)
        self.assertIn("padding-inline-start:1.5em!important", CSS)
        self.assertIn("list-style-position:outside", CSS)

    def test_rtl_geometry_uses_logical_properties_not_physical_padding(self):
        self.assertIn("padding-inline-start:30px;", CSS)
        self.assertIn("border-inline-start:3px solid var(--blue)", CSS)
        # The physical base rules stay, but the scoped overrides must mirror them.
        self.assertIn(".msg-body ul,.msg-body ol{margin:6px 0 10px 20px;", CSS)

    def test_math_diffs_csv_and_tool_output_stay_ltr_under_toggle(self):
        self.assertIn(".chat-content-rtl .msg-body .katex,", CSS)
        self.assertIn(".chat-content-rtl .msg-body .diff-block,", CSS)
        self.assertIn(".chat-content-rtl .msg-body .csv-table,", CSS)
        self.assertIn(".chat-content-rtl .tool-call-group-body,", CSS)
        self.assertIn(".chat-content-rtl .tool-result,", CSS)

    def test_worklog_activity_prose_rows_stay_rtl_under_toggle(self):
        # The activity group body (.tool-call-group-body) also hosts human-language
        # status rows: live thinking text and reasoning summaries. The blanket
        # wildcard LTR on every child mirrored Persian status rows mid-stream
        # (#RTL-worklog). Tool I/O must stay isolated LTR WITHOUT a child wildcard,
        # and prose rows must be re-asserted RTL.
        self.assertNotIn(".chat-content-rtl .tool-call-group-body *,", CSS)
        self.assertIn(".chat-content-rtl .agent-activity-thinking,", CSS)
        self.assertIn(".chat-content-rtl .wl-reason,", CSS)

    def test_plain_stream_chunks_coalesce_into_one_text_node(self):
        self.assertIn("function _smdAppendPlainText", MESSAGES_JS)
        self.assertIn("last.nodeType===3", MESSAGES_JS)
        self.assertIn("last.appendData(value)", MESSAGES_JS)

    def test_live_stream_locks_direction_from_accumulated_first_strong_character(self):
        self.assertIn("function _liveTextDirection", MESSAGES_JS)
        self.assertIn("el.setAttribute('dir',direction)", MESSAGES_JS)
        self.assertIn("_syncLiveAssistantDirection(assistantBody,displayText)", MESSAGES_JS)
        self.assertIn("return 'rtl'", MESSAGES_JS)
        self.assertIn("return 'ltr'", MESSAGES_JS)

    def test_token_handler_locks_direction_before_scheduled_render(self):
        # Direction must update in the SSE token callback itself. Waiting for the
        # throttled rAF/word-fade renderer allows the first Persian glyphs to paint
        # under the previous/automatic bidi state for one visible frame.
        token_handler = MESSAGES_JS.index("source.addEventListener('token',e=>{")
        token_append = MESSAGES_JS.index("assistantText+=d.text;", token_handler)
        row_creation = MESSAGES_JS.index("ensureAssistantRow();", token_append)
        direction_sync = MESSAGES_JS.index(
            "_syncLiveAssistantDirection(assistantBody,_streamDisplay());", token_append
        )
        scheduled_render = MESSAGES_JS.index("_scheduleRender();", token_append)
        self.assertLess(row_creation, direction_sync)
        self.assertLess(direction_sync, scheduled_render)

    def test_settled_render_reapplies_direction_lock_for_live_parity(self):
        # The live→settled handoff rebuilds bodies with dir="auto" only;
        # WebKit then re-resolves direction late and the final frame jumps.
        # renderMessages must re-apply the same first-strong-character lock,
        # so messages.js exports the helper and ui.js consumes it post-render.
        self.assertIn("window._liveTextDirection=_liveTextDirection", MESSAGES_JS)
        self.assertIn("if(inner && typeof _liveTextDirection==='function'){", UI_JS)
        self.assertIn("inner.querySelectorAll('.msg-body').forEach(el=>{", UI_JS)
        self.assertIn("const d=_liveTextDirection(el.textContent);", UI_JS)

    def test_every_live_prose_path_locks_direction(self):
        # The anchor-prose incremental cache bypasses _smdWrite, so creation
        # AND every written delta must lock direction there; the ui.js
        # fallback innerHTML path needs the same lock.
        self.assertIn("const d0=window._liveTextDirection(value);", MESSAGES_JS)
        self.assertIn("const dN=window._liveTextDirection(value);", MESSAGES_JS)
        self.assertIn("const dFb=window._liveTextDirection(text);", UI_JS)

    def test_preview_img_has_no_empty_src_attribute(self):
        # An <img src=""> resolves the EMPTY string against the document URL,
        # so the browser re-requests the whole page as an image and fires a
        # resource error on every load. The attribute must be absent instead;
        # clearing code must use removeAttribute('src'), never src=''.
        self.assertNotIn('id="previewImg" src=""', INDEX_HTML)
        self.assertIn("pi.removeAttribute('src');", BOOT_JS)
        self.assertNotIn("pi.src='';", BOOT_JS)

    def test_persian_locale_bundle_is_registered_after_i18n(self):
        # The fa locale ships as a separate classic script that decorates the
        # global LOCALES after i18n.js loads. It must be included BETWEEN
        # i18n.js and the rest of the app, and must register via _label so the
        # Settings language dropdown (populated from LOCALES) lists فارسی.
        i18n_idx = INDEX_HTML.find('static/i18n.js?')
        fa_idx = INDEX_HTML.find('static/i18n-fa.js?')
        self.assertGreaterEqual(i18n_idx, 0)
        self.assertGreater(fa_idx, i18n_idx)
        self.assertIn("_label = 'فارسی'", I18N_FA)
        self.assertIn("_speech = 'fa-IR'", I18N_FA)

    def test_suggestions_send_their_visible_label(self):
        # Under a non-English locale the suggestion buttons must send their
        # translated visible label, not the hardcoded English data-msg.
        self.assertIn("const seen=(typeof t==='function'&&label)?t(label.getAttribute('data-i18n')):null;", BOOT_JS)
        self.assertIn("(seen&&seen!==label.getAttribute('data-i18n'))?seen:btn.dataset.msg", BOOT_JS)

    def test_ux_hardening_css_contracts(self):
        # Touch targets on coarse pointers; mobile home-indicator clearance;
        # model-picker selected affordance; RTL sidebar bidi details.
        self.assertIn('@media (pointer: coarse){', CSS)
        self.assertIn('.send-btn{width:44px;height:44px;}', CSS)
        self.assertIn('env(safe-area-inset-bottom,0px))!important;}', CSS)
        self.assertIn('.model-opt.active{background:var(--accent-bg);box-shadow:inset 2px 0 0 var(--accent);}', CSS)
        self.assertIn('.suggestion:hover,.suggestion:focus-visible{', CSS)
        self.assertIn('.chat-content-rtl .session-title{text-align:right;', CSS)
        self.assertIn('.chat-content-rtl .model-dropdown{left:auto;right:0;}', CSS)


if __name__ == "__main__":
    unittest.main()
