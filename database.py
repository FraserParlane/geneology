"""Helper functions for db communication"""
import sqlite3
import os


class Database:
    """A helper class for db communication."""
    db_name = 'database.db'
    sql_name = 'database.sql'
    con = None
    cur = None
    connected = False

    def __init__(self):
        pass

    def connect(self):
        """Connect to the database."""
        if not self.connected:
            self.con = sqlite3.connect(self.db_name)
            self.cur = self.con.cursor()
            self.connected = True

    def make_db(self):
        """Create a blank database."""
        self.connect()
        with open(self.sql_name, 'r') as f:
            sql_script = f.read()
        self.cur.executescript(sql_script)
        self.con.commit()


if __name__ == '__main__':
    db = Database()
    db.make_db()
