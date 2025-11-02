import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models, crud
from app.schemas import SweetCreate
from app.database import Base

class TestAdminAndSearch(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        TestingSessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

        # Add sample sweets
        crud.create_sweet(self.db, SweetCreate(name="Ladoo", category="Indian", price=25.0, quantity=10))
        crud.create_sweet(self.db, SweetCreate(name="Donut", category="Western", price=40.0, quantity=5))
        crud.create_sweet(self.db, SweetCreate(name="Barfi", category="Indian", price=15.0, quantity=8))

    def tearDown(self):
        self.db.close()

    def test_search_by_name(self):
        results = crud.search_sweets(self.db, name="lad")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "Ladoo")

    def test_search_by_category(self):
        results = crud.search_sweets(self.db, category="Indian")
        self.assertEqual(len(results), 2)

    def test_search_by_price_range(self):
        results = crud.search_sweets(self.db, min_price=20, max_price=30)
        names = [sweet.name for sweet in results]
        self.assertIn("Ladoo", names)
        self.assertNotIn("Barfi", names)


if __name__ == "__main__":
    unittest.main()
