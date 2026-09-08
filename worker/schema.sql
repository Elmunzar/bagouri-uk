CREATE TABLE IF NOT EXISTS feedback (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  page       TEXT NOT NULL,
  helpful    TEXT,
  confusing  TEXT,
  suggestion TEXT
);
CREATE INDEX IF NOT EXISTS idx_feedback_created ON feedback (created_at);
