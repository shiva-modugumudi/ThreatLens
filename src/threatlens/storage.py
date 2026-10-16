import sqlite3
from datetime import datetime, timezone

SCHEMA = """
CREATE TABLE IF NOT EXISTS indicators (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL,
  value TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending_review' CHECK(status = 'pending_review'),
  first_seen TEXT NOT NULL,
  UNIQUE(kind, value)
);
CREATE TABLE IF NOT EXISTS sightings (
  id INTEGER PRIMARY KEY,
  indicator_id INTEGER NOT NULL REFERENCES indicators(id),
  source TEXT NOT NULL,
  pulse_id TEXT NOT NULL,
  observed_at TEXT NOT NULL,
  UNIQUE(indicator_id, source, pulse_id)
);
CREATE TABLE IF NOT EXISTS audit_events (
  id INTEGER PRIMARY KEY,
  event TEXT NOT NULL,
  details TEXT NOT NULL,
  created_at TEXT NOT NULL
);
"""

class Store:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.executescript(SCHEMA)

    def add(self, kind: str, value: str, pulse_id: str) -> bool:
        now = datetime.now(timezone.utc).isoformat()
        with self.connection:
            cursor = self.connection.execute(
                "INSERT OR IGNORE INTO indicators(kind,value,first_seen) VALUES (?,?,?)",
                (kind, value, now))
            indicator_id = self.connection.execute(
                "SELECT id FROM indicators WHERE kind=? AND value=?", (kind, value)).fetchone()[0]
            self.connection.execute(
                "INSERT OR IGNORE INTO sightings(indicator_id,source,pulse_id,observed_at) VALUES (?,?,?,?)",
                (indicator_id, "AlienVault OTX", pulse_id, now))
            self.connection.execute(
                "INSERT INTO audit_events(event,details,created_at) VALUES (?,?,?)",
                ("ioc_seen", f"{kind}:{value} pulse={pulse_id}", now))
        return cursor.rowcount == 1

    def close(self):
        self.connection.close()
