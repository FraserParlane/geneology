"""Tests"""
from data import Database, Species
import unittest


class TestDatabase(unittest.TestCase):

    def test_database_creation(self):

        db = Database()
        db.make_db()

    def test_insert_taxonomy(self):

        db = Database()
        db.make_db()
        db.insert_taxonomy(
            name='test',
            level=0,
        )
        db.cur.execute('SELECT * FROM taxonomy;')
        rows = db.cur.fetchall()
        assert rows == [(1, 'test', 0, None)]

    def test_get_id(self):
        db = Database()
        db.make_db()
        db.insert_taxonomy(
            name='test',
            level=0,
        )
        id = db.get_id(
            name='test',
            level=0,
        )
        assert isinstance(id, int)

    def test_insert_species(self):

        db = Database()
        db.make_db()
        species = Species(
            taxonomy=[
                'Animalia',
                'Echinodermata',
                'Asteroidea',
                'Valvatida',
                'Asterinidae',
                'Patiria',
                'P. miniata',
            ]
        )
        db.insert_species(species=species)
        db.cur.execute('SELECT id, name, level, parent_id FROM taxonomy;')
        rows = db.cur.fetchall()
        print('a')


if __name__ == '__main__':
    unittest.main()
