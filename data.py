"""Helper functions for db communication"""
from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import sqlite3



@dataclass
class Species:
    """A representation of a species."""
    taxonomy: List[str]

    def __post_init__(self):
        assert len(self.taxonomy) == 7

class Database:
    """A helper class for db communication."""
    db_name = 'database.db'
    sql_name = 'database.sql'
    con = None
    cur = None

    def __init__(self):
        self.connect()

    def connect(self):
        """Connect to the database."""
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()

    def make_db(self):
        """Create a blank database."""
        with open(self.sql_name, 'r') as f:
            sql_script = f.read()
        self.cur.executescript(sql_script)
        self.con.commit()

    def _does_taxonomy_exist(
            self,
            name: str,
            level: int,
    ) -> bool:
        """Test if a taxonomy entry exists."""
        query = f"SELECT * FROM taxonomy WHERE name == '{name}' AND level == '{level}';"
        self.cur.execute(query)
        rows = self.cur.fetchall()
        return False if len(rows) == 0 else True

    def insert_taxonomy(
            self,
            name: str,
            level: int,
            parent_id: Optional[int] = None,
    ):
        """Insert a taxonomy level into the database."""

        # If no parent ID passed, insert NULL into database.
        if parent_id is None:
            parent_id = 'NULL'

        query = f"INSERT INTO taxonomy (name, level, parent_id) VALUES ('{name}', {level}, {parent_id});"
        print(query)
        self.cur.execute(query)
        self.con.commit()

    def insert_species(
            self,
            species: Species,
    ) -> None:
        """Insert a species into the database."""
        self._recur_insert_species(species=species)

    def _recur_insert_species(
            self,
            species: Species,
            level: int = 6,
    ) -> None:

        # If this position doesn't exist
        name = species.taxonomy[level]
        if not self._does_taxonomy_exist(name=name, level=level):

            # Call this function for the parent taxonomy level
            if level != 0:
                self._recur_insert_species(species=species, level=level-1)

            # Insert this position.



if __name__ == '__main__':
    db = Database()
    db.make_db()
