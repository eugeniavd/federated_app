DROP TABLE IF EXISTS events;

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attributedTo TEXT NOT NULL,
    name TEXT, 
    content TEXT NOT NULL,
    startTime TIMESTAMP, 
    location TEXT, 
    published TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP 
);
