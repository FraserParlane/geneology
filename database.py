"""Helper functions for db communication"""
import sqlite3
import os


class Database:
    """A helper class for db communication."""
    db_name = 'database.sqlite'
    con = None
    cur = None
    connected = False

    def __init__(self):
        pass

    def connect(self):
        """Connect to the database."""

        # If already connected, stop.
        if self.connected:
            return

        # If database does not exist, create it.
        if not os.path.exists(self.db_name):
            self.make_db()

        # Connect
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        self.connected = True

    def make_db(self):
        """Create a blank database."""
        ...

if __name__ == '__main__':
    pass