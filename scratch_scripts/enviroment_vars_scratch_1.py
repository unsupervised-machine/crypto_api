from dotenv import load_dotenv
import os

# Path to the .env file relative to the current script
current_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(current_dir, '..', 'env', '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv('API_KEY')
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')

print(f'API_KEY: {API_KEY}')
print(f'MONGO_URI: {MONGO_URI}')
print(f'DATABASE_NAME: {DATABASE_NAME}')
