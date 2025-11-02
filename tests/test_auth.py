import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import models
from app.crud import create_user, authenticate_user
from app.schemas import UserCreate
from app.database import Base


class TestAuth(unittest.TestCase):
    def setUp(self):
        # Use isolated in-memory DB for each run
        self.engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
        TestingSessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()

    def tearDown(self):
        self.db.close()

    def test_user_registration_and_auth(self):
        user_data = UserCreate(username="testuser", password="password123")
        user = create_user(self.db, user_data)
        self.assertEqual(user.username, "testuser")

        auth_user = authenticate_user(self.db, "testuser", "password123")
        self.assertIsNotNone(auth_user)


if __name__ == "__main__":
    unittest.main()
