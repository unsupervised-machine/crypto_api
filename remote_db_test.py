from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import pymongo

import os
from dotenv import load_dotenv
current_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(current_dir, 'env', '.env')
load_dotenv(dotenv_path)

DB_USERNAME = os.getenv('atlas_username')
DB_PASSWORD = os.getenv('atlas_password')


uri = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@cluster0.83a7lsv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


try:
    print('trying to grab example data')
    db = client.get_database('sample_analytics')
    customers = db['customers']
    data = customers.find_one()
    print(data)
except Exception as e:
    print(e)

