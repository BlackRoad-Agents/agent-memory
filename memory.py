#!/usr/bin/env python3
"""Agent Memory System — persistent memory for BlackRoad agents using SQLite."""

import sqlite3
import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

DB_PATH = os.environ.get("AGENT_MEMORY_DB", "agent_memory.db")


class AgentMemory:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE INDEX IF NOT EXISTS idx_agent_key ON memories(agent_id, key);
            CREATE INDEX IF NOT EXISTS idx_agent_time ON memories(agent_id, created_at DESC);
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                agent_id, key, value, content=memories, content_rowid=id
            );
            CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, agent_id, key, value)
                VALUES (new.id, new.agent_id, new.key, new.value);
            END;
            CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, agent_id, key, value)
                VALUES ('delete', old.id, old.agent_id, old.key, old.value);
            END;
            CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, agent_id, key, value)
                VALUES ('delete', old.id, old.agent_id, old.key, old.value);
                INSERT INTO memories_fts(rowid, agent_id, key, value)
                VALUES (new.id, new.agent_id, new.key, new.value);
            END;
        """)
        self.conn.commit()

    def save(self, agent_id: str, key: str, value: Any) -> int:
        """Save a memory. Updates if key exists, inserts otherwise."""
        serialized = json.dumps(value) if not isinstance(value, str) else value
        now = datetime.utcnow().isoformat()
        existing = self.conn.execute(
            "SELECT id FROM memories WHERE agent_id = ? AND key = ?",
            (agent_id, key)
        ).fetchone()
        if existing:
            self.conn.execute(
                "UPDATE memories SET value = ?, updated_at = ? WHERE id = ?",
                (serialized, now, existing["id"])
            )
            self.conn.commit()
            return existing["id"]
        else:
            cur = self.conn.execute(
                "INSERT INTO memories (agent_id, key, value, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (agent_id, key, serialized, now, now)
            )
            self.conn.commit()
            return cur.lastrowid

    def get(self, agent_id: str, key: str) -> Optional[str]:
        """Get a single memory value by key."""
        row = self.conn.execute(
            "SELECT value FROM memories WHERE agent_id = ? AND key = ?",
            (agent_id, key)
        ).fetchone()
        return row["value"] if row else None

    def get_all(self, agent_id: str) -> Dict[str, str]:
        """Get all memories for an agent."""
        rows = self.conn.execute(
            "SELECT key, value FROM memories WHERE agent_id = ? ORDER BY updated_at DESC",
            (agent_id,)
        ).fetchall()
        return {row["key"]: row["value"] for row in rows}

    def search(self, agent_id: str, query: str) -> List[Dict]:
        """Full-text search across an agent's memories."""
        rows = self.conn.execute(
            """SELECT m.key, m.value, m.updated_at
               FROM memories_fts f
               JOIN memories m ON f.rowid = m.id
               WHERE memories_fts MATCH ? AND m.agent_id = ?
               ORDER BY rank
               LIMIT 20""",
            (query, agent_id)
        ).fetchall()
        return [dict(row) for row in rows]

    def get_recent(self, agent_id: str, n: int = 10) -> List[Dict]:
        """Get the N most recently updated memories."""
        rows = self.conn.execute(
            "SELECT key, value, updated_at FROM memories WHERE agent_id = ? ORDER BY updated_at DESC LIMIT ?",
            (agent_id, n)
        ).fetchall()
        return [dict(row) for row in rows]

    def delete(self, agent_id: str, key: str) -> bool:
        """Delete a memory by key."""
        cur = self.conn.execute(
            "DELETE FROM memories WHERE agent_id = ? AND key = ?",
            (agent_id, key)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()


# CLI interface
if __name__ == "__main__":
    import sys
    mem = AgentMemory()
    if len(sys.argv) < 3:
        print("Usage: python memory.py <agent_id> <command> [args...]")
        print("Commands: save <key> <value> | get <key> | all | search <query> | recent [n]")
        sys.exit(1)
    agent = sys.argv[1]
    cmd = sys.argv[2]
    if cmd == "save" and len(sys.argv) >= 5:
        rid = mem.save(agent, sys.argv[3], " ".join(sys.argv[4:]))
        print(f"Saved (id={rid})")
    elif cmd == "get" and len(sys.argv) >= 4:
        val = mem.get(agent, sys.argv[3])
        print(val if val else "(not found)")
    elif cmd == "all":
        for k, v in mem.get_all(agent).items():
            print(f"  {k}: {v}")
    elif cmd == "search" and len(sys.argv) >= 4:
        for r in mem.search(agent, sys.argv[3]):
            print(f"  [{r['updated_at']}] {r['key']}: {r['value']}")
    elif cmd == "recent":
        n = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
        for r in mem.get_recent(agent, n):
            print(f"  [{r['updated_at']}] {r['key']}: {r['value']}")
    else:
        print("Unknown command")
    mem.close()
