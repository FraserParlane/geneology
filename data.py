"""Helper functions for db communication"""
from dataclasses import dataclass
from typing import List, Optional
import pandas as pd
import sqlite3


@dataclass
class Species:
    """A representation of a species."""
    taxonomy: List[str]

    def __post_init__(self):
        assert len(self.taxonomy) == 7
        assert all(isinstance(i, str) for i in self.taxonomy)


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
        self.cur.execute(query)
        self.con.commit()

    def get_id(
            self,
            name: str,
            level: int,
    ) -> int:
        """Get the ID for a given name, level."""
        query = f"SELECT id FROM taxonomy WHERE name == '{name}' AND level == '{level}';"
        self.cur.execute(query)
        rows = self.cur.fetchall()

        # Confirm only one ID returned
        assert len(rows) == 1
        assert len(rows[0]) == 1
        tax_id = rows[0][0]
        return tax_id

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
        """Recursively insert species taxonomy into the database, as needed."""

        # If this position doesn't exist
        name = species.taxonomy[level]
        if not self._does_taxonomy_exist(name=name, level=level):

            # Call this function recursively for the parent taxonomy level.
            parent_id = 'NULL'
            if level != 0:
                parent_level = level - 1
                self._recur_insert_species(species=species, level=parent_level)

                # Get Parent ID
                parent_id = self.get_id(
                    name=species.taxonomy[parent_level],
                    level=parent_level,
                )

            # Insert this position.
            self.insert_taxonomy(
                name=name,
                level=level,
                parent_id=parent_id,
            )

    def get_parent_ids(
            self,
            tax_id: int,
    ) -> List[int]:
        """For a given ID, get all parent IDs."""

        ids = [tax_id]
        while True:

            # Get parent ID
            query = f"SELECT parent_id FROM taxonomy WHERE id == '{tax_id}';"
            self.cur.execute(query)
            row = self.cur.fetchone()
            tax_id = row[0]

            # If no parent ID, break loop
            if tax_id is None:
                break

            # Store parent ID
            ids.append(tax_id)

        # Order such that the greatest ancestor is first.
        ids = ids[::-1]
        return ids

    def get_df(self):
        """Return the database as a dataframe."""
        query = 'SELECT * FROM taxonomy;'
        df = pd.read_sql_query(query, self.con)
        df['parent_id'] = df['parent_id'].astype('Int64')
        return df


if __name__ == '__main__':
    pass
