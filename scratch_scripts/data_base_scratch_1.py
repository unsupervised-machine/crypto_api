from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["crypto_api_db"]
test_collection = db['collection_1']

# Example Document
btc_data = {
    "name": "Bitcoin",
    "symbol": "BTC",
}

btc_id = test_collection.insert_one(btc_data).inserted_id
print(f'Inserted bitcoin with id: {btc_id}')