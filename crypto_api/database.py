import json

import pymongo
from bson.objectid import ObjectId
import os
from crypto_api import api_client

from dotenv import load_dotenv

current_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(current_dir, '..', 'env', '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv('API_KEY')
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')


# MongoDB connection
client = pymongo.MongoClient(MONGO_URI)
db = client.get_database(DATABASE_NAME)

# Collections
current_only = db["current_only"]
cryptocurrencies = db["cryptocurrencies"]
price_history = db["price_history"]
users = db["users"]
favorites = db["favorites"]


# Create instance of api_client
client = api_client.CoinGeckoClient()


def insert_cryptocurrency(data):
    return cryptocurrencies.insert_one(data)


def get_cryptocurrency_by_id(crypto_id):
    return cryptocurrencies.find_one({"_id": ObjectId(crypto_id)})


def get_all_cryptocurrencies():
    return cryptocurrencies.find()


def insert_price_history(data):
    return price_history.insert_one(data)


def fetch_and_store_current_data():
    """
    replaces data in current_only collection in database with fresh data
    :return:
    """
    # Clear collection
    current_only.delete_many({})

    # Get new data from api
    market_data = client.get_cryptocurrencies(sparkline=True)
    print(market_data)

    # Insert new data into collection
    current_only.insert_many(market_data)

# schedule.every(5).minutes.do(fetch_and_store_current_data)


def get_all_records(collection):
    cursor = collection.find({})
    return list(cursor)


def save_to_file(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=2, default=str)


if __name__ == "__main__":
    fetch_and_store_current_data()
    currencies = get_all_records(current_only)
    save_to_file("../src/MOCK_DATA.json", currencies)
