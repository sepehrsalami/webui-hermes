"""Regression contract: a settled large turn must remain visible."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MESSAGES = (ROOT / "static/messages.js").read_text(encoding="utf-8")
UI = (ROOT / "static/ui.js").read_text(encoding="utf-8")


class StreamDoneFollowTests(unittest.TestCase):
    def test_ui_exposes_monotonic_reader_scroll_generation(self):
        self.assertIn("function _messageScrollInputGenerationValue()", UI)
        self.assertIn("return _messageScrollInputGeneration;", UI)

    def test_fresh_stream_captures_reader_scroll_generation_after_reset(self):
        reset = MESSAGES.index("_resetStreamScrollFollow()")
        capture = MESSAGES.index("const _streamScrollInputGenerationAtAttach=")
        self.assertLess(reset, capture)
        self.assertIn("!reconnecting", MESSAGES[capture:capture + 500])

    def test_done_follows_tail_when_no_real_reader_scroll_happened(self):
        self.assertIn("const noReaderScrollSinceStreamStart=", MESSAGES)
        self.assertIn("_streamScrollInputGenerationAtAttach!==null", MESSAGES)
        self.assertIn("_messageScrollInputGenerationValue()===_streamScrollInputGenerationAtAttach", MESSAGES)
        self.assertIn("noReaderScrollSinceStreamStart", MESSAGES[MESSAGES.index("const shouldFollowOnDone="):MESSAGES.index("const _settledStreamId=")])

    def test_reconnected_stream_does_not_force_follow(self):
        capture = MESSAGES.index("const _streamScrollInputGenerationAtAttach=")
        self.assertIn("!reconnecting", MESSAGES[capture:capture + 500])


if __name__ == "__main__":
    unittest.main()
