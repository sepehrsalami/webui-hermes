import sqlite3

from api import routes


def _seed_state_db(path):
    conn = sqlite3.connect(path)
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


def test_raw_all_sidebar_payload_keeps_native_webui_rows_actionable(tmp_path):
    db_path = tmp_path / "state.db"
    _seed_state_db(db_path)

    payload = routes._raw_all_session_sidebar_payload(db_path, profile="default")

    assert [row["session_id"] for row in payload["sessions"]] == [
        "sub-1", "web-1", "telegram-1"
    ]
    rows = {row["session_id"]: row for row in payload["sessions"]}
    assert rows["web-1"]["read_only"] is False
    assert rows["sub-1"]["read_only"] is True
    assert rows["telegram-1"]["read_only"] is True
    assert payload["sessions"][0]["parent_session_id"] == "web-1"
    assert payload["sessions"][0]["title"] == "Subagent Session"
    assert payload["include_archived"] is True
    assert payload["raw_all"] is True
    assert payload["total_count"] == 3
    assert not any(row["source_tag"] == "cron" for row in payload["sessions"])


def test_raw_all_sidebar_payload_missing_database_is_empty(tmp_path):
    payload = routes._raw_all_session_sidebar_payload(tmp_path / "missing.db", profile="default")
    assert payload["sessions"] == []
    assert payload["total_count"] == 0
    assert payload["raw_all"] is True
