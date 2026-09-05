// Persian (fa) locale — high-traffic keys; missing keys fall back to English.
// Added during the 2026-08-24 RTL/UX pass so the empty state, sidebar buckets,
// composer, and model picker render natively in Persian under the RTL toggle.
// Load AFTER i18n.js (classic script): reads the global LOCALES and registers
// itself — the Settings language dropdown lists locales straight from LOCALES,
// so "فارسی" appears automatically.
(function () {
  var faExtra = {
    // Empty state + suggestions
    empty_title: 'در چه خدمتی باشم؟',
    empty_subtitle: 'هر چیزی بپرس، دستور اجرا کن، فایل‌ها را بگرد، یا کارهای زمان‌بندی‌شده را مدیریت کن.',
    suggest_files: 'چه فایل‌هایی در این ورک‌اسپیس هست؟',
    suggest_schedule: 'برنامه امروز من چه است؟',
    suggest_plan: 'در برنامه‌ریزی یک پروژه کوچک کمکم کن.',
    // Sidebar
    filter_conversations: 'فیلتر گفتگوها…',
    session_time_bucket_today: 'امروز',
    session_time_bucket_yesterday: 'دیروز',
    session_time_bucket_this_week: 'این هفته',
    session_time_bucket_last_week: 'هفته پیش',
    session_time_bucket_older: 'قدیمی‌تر',
    session_time_minutes_ago: function (n) { return n + 'د'; },
    tab_chat: 'گفتگو',
    untitled: 'بدون عنوان',
    // Composer / send
    composer_send: 'ارسال پیام',
    clarify_send: 'ارسال',
    composer_control_attach: 'پیوست فایل',
    thinking: 'در حال فکر کردن…',
    cancel: 'لغو',
    // Model picker
    model_search_placeholder: 'جستجوی مدل…',
    model_custom_placeholder: 'مثلاً openai/gpt-5.4'
  };
  if (typeof LOCALES === 'undefined' || LOCALES.fa) return;
  var fa = Object.assign({}, LOCALES.en); // shallow copy → every EN key resolves
  Object.assign(fa, faExtra);
  fa._lang = 'fa';
  fa._label = 'فارسی';
  fa._speech = 'fa-IR';
  LOCALES.fa = fa;
  // i18n.js resolves the saved language during ITS own body — before this file
  // registers fa — and setLocale() then PERSISTS the resolved fallback ('en'),
  // overwriting a stored 'fa' preference. The capture script in index.html
  // snapshots the raw stored value before that happens; re-resolve it here.
  try {
    var stored = (typeof window !== 'undefined' && window.__hermesLangStored) || null;
    if (stored && String(stored).toLowerCase().indexOf('fa') === 0 && typeof setLocale === 'function') {
      setLocale('fa');
      if (typeof applyLocaleToDOM === 'function') applyLocaleToDOM();
    }
  } catch (_) {}
})();
