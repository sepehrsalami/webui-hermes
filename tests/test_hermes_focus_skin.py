import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "static/index.html").read_text(encoding="utf-8")
BOOT = (ROOT / "static/boot.js").read_text(encoding="utf-8")
COMMANDS = (ROOT / "static/commands.js").read_text(encoding="utf-8")
CSS = re.sub(r"\s+", "", (ROOT / "static/style.css").read_text(encoding="utf-8"))


class HermesFocusSkinTests(unittest.TestCase):
    def test_focus_is_a_selectable_persistent_skin(self):
        self.assertRegex(INDEX, r"skins=\{[^}]*focus:1")
        self.assertIn("{name:'Hermes Focus', value:'focus'", BOOT)
        self.assertIn("const skins=(_SKINS||[]).map", COMMANDS)

    def test_blue_is_a_selectable_persistent_palette_for_focus_layout(self):
        config = (ROOT / "api/config.py").read_text(encoding="utf-8")
        self.assertRegex(INDEX, r"skins=\{[^}]*blue:1")
        self.assertIn("{name:'Blue', value:'blue'", BOOT)
        self.assertIn('"blue",', config)
        self.assertIn("const useFocusLayout=key==='focus'||key==='blue';", BOOT)
        self.assertIn("document.documentElement.dataset.skin='focus';", BOOT)
        self.assertIn("document.documentElement.dataset.palette='blue';", BOOT)
        self.assertIn(':root[data-skin="focus"][data-palette="blue"]{', CSS)
        self.assertIn('--accent:#0a6ee8', CSS)
        self.assertIn('--focus-composer-border:#0a84ff', CSS)
        self.assertIn(':root.dark[data-skin="focus"][data-palette="blue"]{', CSS)

    def test_server_selected_skin_including_default_wins_over_stale_browser_cache(self):
        self.assertIn("const skin=lsSkinIsPendingExt?lsSkin:srvAppearance.skin;", BOOT)
        self.assertNotIn("shouldPushLocalSkin", BOOT)
        self.assertNotIn("srvHasExplicitSkin", BOOT)

    def test_focus_changes_chrome_not_message_rendering(self):
        focus_css = CSS.split('/*──Skin:HermesFocus', 1)[1].split('/*──Skin:Catppuccin', 1)[0]
        self.assertNotIn('.msg-body', focus_css)
        self.assertNotIn('.msg-row', focus_css)
        self.assertNotIn('unicode-bidi', focus_css)
        self.assertNotIn('direction:rtl', focus_css)
        self.assertNotIn('direction:ltr', focus_css)

    def test_focus_uses_reading_first_geometry(self):
        self.assertIn(':root[data-skin="focus"]{', CSS)
        self.assertIn(':root[data-skin="focus"].sidebar{width:256px', CSS)
        self.assertIn(':root[data-skin="focus"].messages-inner{max-width:840px', CSS)
        self.assertIn(':root[data-skin="focus"].composer-box{max-width:840px', CSS)

    def test_focus_chat_sidebar_has_a_compact_single_action_header(self):
        self.assertIn('id="focusConversationLabel"', INDEX)
        self.assertIn('id="btnNewChat"', INDEX)
        self.assertIn(':root[data-skin="focus"]#panelChat>.panel-head{min-height:42px', CSS)
        self.assertIn(':root[data-skin="focus"]#panelChat>.panel-head.panel-head-actions{gap:4px', CSS)

    def test_focus_sidebar_reduces_session_noise_without_removing_state(self):
        sessions = (ROOT / "static/sessions.js").read_text(encoding="utf-8")
        self.assertIn("function _isFocusSidebarMode()", sessions)
        self.assertIn("if(!_isFocusSidebarMode()) qs.set('sidebar_source'", sessions)
        self.assertIn("if(!_isFocusSidebarMode()&&_sessionListExcludeHiddenEnabled())", sessions)
        self.assertIn("const focusSidebar=_isFocusSidebarMode();", sessions)
        self.assertIn("if(!focusSidebar&&(window._showCliSessions || cliSessionCount>0))", sessions)
        self.assertIn("if(!focusSidebar&&(_allProjects.length>0||hasUnprojected))", sessions)
        self.assertIn("const groups=focusSidebar", sessions)
        self.assertIn("if(!focusSidebar) wrapper.appendChild(hdr);", sessions)
        self.assertIn(':root[data-skin="focus"].session-source-chip{display:none', CSS)
        self.assertIn(':root[data-skin="focus"].session-item.active{background:var(--focus-session-active);box-shadow:none;color:var(--text)', CSS)
        self.assertIn(':root[data-skin="focus"].session-item.active.session-title{color:var(--text)!important', CSS)
        self.assertIn(':root[data-skin="focus"].session-item.active.session-meta{color:var(--muted2)!important', CSS)

    def test_focus_sidebar_hides_child_counts_and_child_rows(self):
        sessions = (ROOT / "static/sessions.js").read_text(encoding="utf-8")
        self.assertIn("const childCount=focusSidebar?0:", sessions)
        self.assertIn(':root[data-skin="focus"].session-child-count{display:none', CSS)
        self.assertIn(':root[data-skin="focus"].session-child-sessions{display:none', CSS)

    def test_focus_composer_uses_discord_inspired_focus_treatment(self):
        self.assertIn('--focus-composer-border:rgba(78,80,88,.48)', CSS)
        self.assertIn('--focus-composer-border-active:#5865f2', CSS)
        self.assertIn(':root[data-skin="focus"].composer-box{max-width:840px;border:1pxsolidvar(--focus-composer-border)!important', CSS)
        self.assertIn(':root[data-skin="focus"].composer-box:focus-within{border-color:var(--focus-composer-border-active)!important;box-shadow:0003pxvar(--focus-ring)!important', CSS)
        self.assertIn(':root[data-skin="focus"].composer-wrap.drag-over.composer-box{border-color:var(--focus-composer-border-active)!important;box-shadow:0003pxvar(--focus-ring)!important', CSS)

    def test_focus_has_discord_inspired_layered_surfaces_and_accessible_states(self):
        self.assertIn('--focus-rail:#1e1f22', CSS)
        self.assertIn('--focus-sidebar:#2b2d31', CSS)
        self.assertIn('--focus-chat:#313338', CSS)
        self.assertIn('--accent:#5865f2', CSS)
        self.assertIn(':root[data-skin="focus"].rail-btn.active{background:var(--accent)', CSS)
        self.assertIn(':root[data-skin="focus"]:is(button,a,input,textarea,select):focus-visible{outline:2pxsolidvar(--focus-ring)', CSS)
        self.assertIn(':root[data-skin="focus"]{overflow-x:clip', CSS)
        self.assertIn(':root[data-skin="focus"]body{overflow-x:clip', CSS)
        self.assertIn('@media(prefers-reduced-motion:reduce){:root[data-skin="focus"]*{scroll-behavior:auto!important;transition-duration:.01ms!important', CSS)

    def test_focus_light_mode_keeps_the_same_layer_hierarchy(self):
        self.assertIn(':root:not(.dark)[data-skin="focus"]{', CSS)
        self.assertIn('--focus-rail:#e3e5e8', CSS)
        self.assertIn('--focus-sidebar:#f2f3f5', CSS)
        self.assertIn('--focus-chat:#ffffff', CSS)

    def test_focus_composer_matches_the_reference_control_hierarchy(self):
        self.assertIn(':root[data-skin="focus"]#btnAttachsvg{display:none', CSS)
        self.assertIn(':root[data-skin="focus"]#btnAttach::before{content:"+"', CSS)
        self.assertIn(':root[data-skin="focus"]#btnAttach::after{display:none!important', CSS)
        self.assertIn(':root[data-skin="focus"]#btnSavedPrompts{display:none!important', CSS)
        self.assertIn(':root[data-skin="focus"].composer-reasoning-wrap{order:80', CSS)
        self.assertIn(':root[data-skin="focus"]#btnMic{order:90', CSS)
        self.assertIn(':root[data-skin="focus"]#btnVoiceMode{order:91', CSS)
        boot = (ROOT / "static/boot.js").read_text(encoding="utf-8")
        self.assertIn("msg.placeholder=_isFocusAppearance()?'Ask anything'", boot)

    def test_focus_session_menu_is_share_rename_pin_archive_delete(self):
        sessions = (ROOT / "static/sessions.js").read_text(encoding="utf-8")
        self.assertIn("function _appendFocusSessionActions(menu, session, anchorEl)", sessions)
        self.assertIn("if(_isFocusSidebarMode()){", sessions)
        self.assertIn("_appendFocusSessionActions(menu,session,anchorEl);", sessions)
        self.assertIn("className='session-action-separator'", sessions)
        for label in ("share_session", "session_rename", "session_pin", "session_archive", "session_delete"):
            self.assertIn(f"t('{label}')", sessions)
        self.assertIn(':root[data-skin="focus"].session-action-menu{min-width:210px', CSS)
        self.assertIn(':root[data-skin="focus"].session-action-separator{height:1px', CSS)
        self.assertIn(':root[data-skin="focus"].session-item.active.session-actions{opacity:1;pointer-events:auto', CSS)

    def test_applying_focus_layout_immediately_resyncs_dependent_ui(self):
        boot = (ROOT / "static/boot.js").read_text(encoding="utf-8")
        ui = (ROOT / "static/ui.js").read_text(encoding="utf-8")
        self.assertIn("if(useFocusLayout&&typeof renderSessionListFromCache==='function')", boot)
        self.assertIn("if(msg&&useFocusLayout) msg.placeholder='Ask anything';", boot)
        self.assertIn("const idlePlaceholder=document.documentElement.dataset.skin==='focus'", ui)

    def test_focus_treats_native_webui_rows_as_actionable_before_server_restart(self):
        sessions = (ROOT / "static/sessions.js").read_text(encoding="utf-8")
        self.assertIn("function _isFocusNativeWebuiSession(session)", sessions)
        self.assertIn("const readOnly=_isReadOnlySession(s)&&!_isFocusNativeWebuiSession(s);", sessions)
        self.assertIn("if(_isReadOnlySession(session)&&!_isFocusNativeWebuiSession(session))", sessions)

    def test_focus_sidebar_stays_full_width_on_mobile_overlay(self):
        self.assertIn('@media(max-width:640px){:root[data-skin="focus"].sidebar{width:100vw', CSS)

    def test_focus_uses_progressive_disclosure_without_deleting_controls(self):
        self.assertIn('id="focusComposerControlsBtn"', INDEX)
        self.assertIn(':root[data-skin="focus"]#focusComposerControlsBtn{display:flex', CSS)
        self.assertIn(':root[data-skin="focus"].composer-left>:is(.composer-divider,.yolo-pill,.composer-profile-wrap,.composer-ws-wrap,.composer-model-wrap,.provider-quota-chip,.composer-toolsets-wrap){visibility:hidden', CSS)
        self.assertIn(':root[data-skin="focus"].composer-footer.focus-advanced.composer-left>:is(.composer-divider,.yolo-pill,.composer-profile-wrap,.composer-ws-wrap,.composer-model-wrap,.provider-quota-chip,.composer-reasoning-wrap,.composer-toolsets-wrap){visibility:visible', CSS)
        for control_id in (
            'profileChip', 'composerWorkspaceChip', 'composerModelChip',
            'composerReasoningChip', 'composerToolsetsChip', 'ctxIndicator'
        ):
            self.assertIn(f'id="{control_id}"', INDEX)

    def test_focus_rail_prioritizes_chat_tasks_workspace_and_settings(self):
        self.assertIn(':root[data-skin="focus"].rail.nav-tab[data-panel="chat"]', CSS)
        self.assertIn(':root[data-skin="focus"].rail.nav-tab[data-panel="tasks"]', CSS)
        self.assertIn(':root[data-skin="focus"].rail.nav-tab[data-panel="workspaces"]', CSS)
        self.assertIn(':root[data-skin="focus"].rail.nav-tab[data-panel="settings"]', CSS)
        self.assertIn(':root[data-skin="focus"].rail.nav-tab:not([data-panel="chat"]):not([data-panel="tasks"]):not([data-panel="workspaces"]):not([data-panel="settings"]){display:none;}', CSS)
        self.assertIn(':root[data-skin="focus"].rail.focus-more-open.nav-tab:not([data-panel="settings"]){display:flex;}', CSS)
        self.assertIn('id="focusRailMoreBtn"', INDEX)

    def test_focus_preserves_bidirectional_content_contracts(self):
        self.assertIn('.chat-content-rtl.msg-row[data-role="assistant"].msg-body{', CSS)
        self.assertIn('.chat-content-rtl.msg-body:is(ul,ol){', CSS)
        self.assertIn('unicode-bidi:isolate', CSS)
        self.assertIn('direction:ltr', CSS)

    def test_dirty_frontend_changes_get_a_content_fingerprinted_asset_version(self):
        routes = (ROOT / "api/routes.py").read_text(encoding="utf-8")
        self.assertIn("def _webui_asset_version", routes)
        self.assertIn("_WEBUI_ASSET_FINGERPRINT_PATHS", routes)
        self.assertIn('replace("__WEBUI_VERSION__", asset_version_token)', routes)
        self.assertIn('settings["asset_version"] = _webui_asset_version()', routes)


if __name__ == "__main__":
    unittest.main()
