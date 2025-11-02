import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.crud import create_sweet, get_sweet_by_id
from app.schemas import SweetCreate
from app.database import Base


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        TestingSessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_purchase_and_restock(self):
        sweet = create_sweet(self.db, SweetCreate(name="Barfi", category="Indian", price=15.0, quantity=10))
        sweet.quantity -= 1
        self.db.commit()
        updated = get_sweet_by_id(self.db, sweet.id)
        self.assertEqual(updated.quantity, 9)


if __name__ == "__main__":
    unittest.main()
