import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.crud import create_sweet, get_sweets
from app.schemas import SweetCreate
from app.database import Base


class TestSweetCRUD(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        TestingSessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_create_and_get_sweets(self):
        sweet_data = SweetCreate(name="Ladoo", category="Indian", price=25.0, quantity=30)
        sweet = create_sweet(self.db, sweet_data)
        self.assertEqual(sweet.name, "Ladoo")

        sweets = get_sweets(self.db)
        self.assertTrue(len(sweets) >= 1)


if __name__ == "__main__":
    unittest.main()
