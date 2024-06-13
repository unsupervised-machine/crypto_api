import unittest
from pymongo import MongoClient
from crypto_api import database

from dotenv import load_dotenv
import os

current_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(current_dir, '..', 'env', '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv('API_KEY')
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = 'test_db'

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to a test database
        cls.client = MongoClient(MONGO_URI)
        cls.db = cls.client[DATABASE_NAME]
        database.cryptocurrencies = cls.db["cryptocurrencies"]
        # Initialize test data if needed

    @classmethod
    def tearDownClass(cls):
        # Clean up after tests
        cls.client.drop_database('test_db')
        cls.client.close()

    def test_insert_cryptocurrency(self):
        data = {
            "name": "Bitcoin",
            "symbol": "BTC",
            "image_url": "https://example.com/bitcoin.png"
        }
        result = database.insert_cryptocurrency(data)
        self.assertIsNotNone(result.inserted_id)

        # Optionally, you can verify the inserted document
        inserted_doc = self.db.cryptocurrencies.find_one({"name": "Bitcoin"})
        self.assertIsNotNone(inserted_doc)
        self.assertEqual(inserted_doc["name"], "Bitcoin")
        self.assertEqual(inserted_doc["symbol"], "BTC")
        self.assertEqual(inserted_doc["image_url"], "https://example.com/bitcoin.png")

    # Add more tests for other database functions

if __name__ == '__main__':
    unittest.main()

