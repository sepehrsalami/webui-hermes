import sqlite3
import tempfile
import unittest
from pathlib import Path

from api import routes


class RawAllSessionSidebarTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmp.name) / "state.db"
        conn = sqlite3.connect(self.db_path)
        conn.executescript(
            """
            CREATE TABLE sessions (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                title TEXT,
                model TEXT,
                message_count INTEGER DEFAULT 0,
                started_at REAL NOT NULL,
                last_activity_at REAL,
                parent_session_id TEXT,
                archived INTEGER DEFAULT 0
            );
            """
        )
        conn.executemany(
            "INSERT INTO sessions (id, source, title, model, message_count, started_at, last_activity_at, parent_session_id, archived) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("web-1", "webui", "Web chat", "m", 3, 10.0, 12.0, None, 0),
                ("cron-1", "cron", "Cron run", "m", 4, 20.0, 22.0, None, 0),
                ("sub-1", "subagent", None, "m", 5, 30.0, 32.0, "web-1", 0),
                ("telegram-1", "telegram", "Old Telegram", "m", 6, 5.0, 6.0, None, 1),
            ],
        )
        conn.commit()
        conn.close()

    def tearDown(self):
        self.tmp.cleanup()

    def test_returns_every_state_db_row_with_native_webui_actions(self):
        payload = routes._raw_all_session_sidebar_payload(self.db_path, profile="default")
        self.assertEqual(
            [row["session_id"] for row in payload["sessions"]],
            ["sub-1", "web-1", "telegram-1"],
        )
        rows = {row["session_id"]: row for row in payload["sessions"]}
        self.assertFalse(rows["web-1"]["read_only"])
        self.assertTrue(rows["sub-1"]["read_only"])
        self.assertTrue(rows["telegram-1"]["read_only"])
        self.assertEqual(payload["sessions"][0]["parent_session_id"], "web-1")
        self.assertEqual(payload["sessions"][0]["title"], "Subagent Session")
        self.assertTrue(payload["include_archived"])
        self.assertTrue(payload["raw_all"])
        self.assertEqual(payload["total_count"], 3)
        self.assertFalse(any(row["source_tag"] == "cron" for row in payload["sessions"]))

    def test_missing_database_is_empty(self):
        payload = routes._raw_all_session_sidebar_payload(Path(self.tmp.name) / "missing.db", profile="default")
        self.assertEqual(payload["sessions"], [])
        self.assertEqual(payload["total_count"], 0)
        self.assertTrue(payload["raw_all"])


if __name__ == "__main__":
    unittest.main()
