CREATE TABLE IF NOT EXISTS web_password (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostName TEXT NOT NULL,
    password TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)