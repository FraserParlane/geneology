DROP TABLE IF EXISTS taxonomy;
CREATE TABLE taxonomy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    parent_id INTEGER,
    name VARCHAR(255) NOT NULL,
    level INTEGER NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES taxonomy(id)
);