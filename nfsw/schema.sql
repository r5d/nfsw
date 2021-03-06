DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  terms_agreed INTEGER DEFAULT 0,
  last_login TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
