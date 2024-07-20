import json
from datetime import datetime
from passlib.context import CryptContext


import pymongo
from bson.objectid import ObjectId
import os
from crypto_api import api_client

from dotenv import load_dotenv


ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

current_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(current_dir, '..', 'env', '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv('API_KEY')
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')


# MongoDB connection
db_client = pymongo.MongoClient(MONGO_URI)
db = db_client.get_database(DATABASE_NAME)

# Collections
current_only = db["current_only"]
cryptocurrencies = db["cryptocurrencies"]
portfolios = db["portfolios"]
price_history = db["price_history"]
users = db["users"]
favorites = db["favorites"]


# Create instance of api_client
cg_client = api_client.CoinGeckoClient()


# -- Helper Funtions -- #
def get_all_records(collection):
    cursor = collection.find({})
    return list(cursor)


# -- Passwords and Hashing -- #
def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# -- Users -- #
def insert_user(email, first_name, last_name, username, password):
    try:
        # Create the document to insert
        hashed_password = get_password_hash(password)
        create_user_timestamp = datetime.now()
        disabled_status = False
        user_data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "hashed_password": hashed_password,
            "disabled": disabled_status,
            "created_at": create_user_timestamp,
            "updated_at": create_user_timestamp,
        }

        # Preform insertion
        insert_result = users.insert_one(user_data)

        # Check if insertion was successful
        if insert_result.acknowledged:
            print("User inserted successfully. Inserted id:", insert_result.inserted_id)
            return True  # Or you can return the inserted_id or another indicator of success
        else:
            print("Insert failed.")
            return False

    except pymongo.errors.DuplicateKeyError as e:
        # Handle duplicate key error specifically
        print(f"Duplicate key error: {e}")
        return "Duplicate key error"
    except pymongo.errors.PyMongoError as e:
        # Handle other MongoDB errors
        print(f"An error occurred: {e}")
        return "Database error"
    # finally:
    #     # Close client if it's a local client
    #     db_client.close()


def get_all_users():
    """Returns a dict of all users"""
    res = get_all_records(collection=users)
    return res


def get_user(username):
    """If not found, returns None"""
    return users.find_one({"username": username})


# -- Cryptocurrencies -- #

def insert_cryptocurrency(data):
    return cryptocurrencies.insert_one(data)


def get_cryptocurrency_by_id(crypto_id):
    return cryptocurrencies.find_one({"_id": ObjectId(crypto_id)})


def get_all_cryptocurrencies():
    return cryptocurrencies.find()


def get_all_current_only():
    cursor = current_only.find(
        {},
        { "_id": 0},
    )
    documents = list(cursor)
    return documents


def insert_price_history(data):
    return price_history.insert_one(data)


# -- Favorites -- #
def update_portfolio(username: str, set_favorites: list):
    portfolios.update_one(
        { "_id": username },
        # { "$push": { "favorites": { "$each": add_to_favorites}  } },
        {"$set": {"favorites": set_favorites}},
        upsert=True
    )


def get_user_portfolio(username: str):
    """

    :param username:
    :return: {'favorites': ['example 1', 'example 2', ... ]}
    """

    favorites_data = portfolios.find_one(
        { "_id": username },
        { "favorites": 1 , "_id": 0}
    )
    return favorites_data


# -- Refreshing -- #
def update_current_only_data():
    """
    replaces data in current_only collection in database with fresh data
    :return:
    """
    print("Inside fetch_and_store")
    # Clear collection
    # print(get_all_records(current_only))
    current_only.delete_many({})
    # print(get_all_records(current_only))

    # Get new data from api
    market_data = cg_client.get_cryptocurrencies(sparkline=True)
    # print(market_data)

    # Insert new data into collection
    current_only.insert_many(market_data)
    # print(get_all_records(current_only))

# schedule.every(5).minutes.do(update_current_only_data)


def save_to_file(file_name, data):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=2, default=str)


# -- Testing -- #
def create_mock_data():
    update_current_only_data()
    currencies = get_all_records(current_only)
    save_to_file("../data/MOCK_DATA_2.json", currencies)


def insert_mock_user():
    # email, first_name, last_name, username, password
    insert_user("taran123@gmail.com", "Taran", "Lau", 'taran50', "123")


def test_get_all_users():
    test = get_all_users()
    print(test)


def test_get_user():
    username = "taran50"
    user = get_user(username)
    print(user)


def test_password_hash():
    password = "123"
    hashed_password = get_password_hash(password)
    print(password)
    print(hashed_password)

    is_correct = verify_password(password, hashed_password)
    print("is correct ", is_correct)


def test_password_hash_2():
    print("entering 2nd test_password_hash_2")
    password = "123"
    hashed_password = "$2b$12$C9CRkEpVv1TW4Ym8ZHR3ReBxZSW6u8Fx.1U0cdnNxhtGEf9OdMIx2"
    is_correct = verify_password(password, hashed_password)
    print("is correct ", is_correct)


def test_update_portfolio():
    username = "taran50"
    add_to_favorites = ['bitcoin', 'ethereum']
    update_portfolio(username, add_to_favorites)


def test_get_user_portfolio():
    username = "taran50"
    print(get_user_portfolio(username))


if __name__ == "__main__":
    print(get_all_current_only())
    # update_current_only_data()
    # create_mock_data()
    # insert_mock_user()
    # test_get_all_users()
    # test_get_user()
    # test_password_hash()
    # test_password_hash_2()
    # test_update_portfolio()
    # test_get_user_portfolio()
