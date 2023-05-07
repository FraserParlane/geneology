"""Tests"""
from data import Database, Species
import unittest


class TestDatabase(unittest.TestCase):

    species_a = Species(
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

    species_b = Species(
        taxonomy=[
            'Animalia',
            'Echinodermata',
            'Asteroidea',
            'Forcipulatida',
            'Asteriidae',
            'Leptasterias',
            'L. polaris',
        ]
    )

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
        tax_id = db.get_id(
            name='test',
            level=0,
        )
        assert isinstance(tax_id, int)

    def test_insert_species(self):

        db = Database()
        db.make_db()
        db.insert_species(species=self.species_a)
        db.insert_species(species=self.species_b)
        db.cur.execute('SELECT id, name, level, parent_id FROM taxonomy;')
        rows = db.cur.fetchall()
        assert len(rows) == 11

    def test_get_parent_ids(self):
        db = Database()
        db.make_db()
        db.insert_species(species=self.species_a)
        ids = db.get_parent_ids(tax_id=5)
        assert len(ids) == 5

    def test_database_to_dataframe(self):
        db = Database()
        db.make_db()
        db.insert_species(species=self.species_a)
        db.insert_species(species=self.species_b)
        df = db.get_df()
        assert len(df) == 11


if __name__ == '__main__':
    unittest.main()
