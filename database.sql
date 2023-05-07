DROP TABLE IF EXISTS taxonomy;
CREATE TABLE taxonomy (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    level INTEGER NOT NULL,
    parent_id INTEGER,
    FOREIGN KEY (parent_id) REFERENCES taxonomy(id)
);