from bson import ObjectId
from fastapi import FastAPI, HTTPException
from crypto_api import database
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List


app = FastAPI()


class CryptoCurrency(BaseModel):
    name: str
    symbol: str
    image_url: str


# Example endpoint to get cryptocurrency by ID
@app.get('/api/cryptocurrency/{crypto_id}')
async def get_cryptocurrency(crypto_id: str):
    # Convert crypto_id to ObjectId if needed (example assuming MongoDB)
    try:
        crypto_data = database.get_cryptocurrency_by_id(ObjectId(crypto_id))
        # Convert ObjectId to string for JSON serialization
        crypto_data['_id'] = str(crypto_data['_id'])
        print(f'crypto_data: {crypto_data}')
    except Exception as e:
        raise HTTPException(status_code=404, detail="Cryptocurrency not found")

    if crypto_data:
        return crypto_data
    else:
        raise HTTPException(status_code=404, detail="Cryptocurrency not found")


@app.get('/api/cryptocurrencies')
async def get_all_cryptocurrencies():
    all_cryptocurrencies = []
    collection = database.get_all_cryptocurrencies()
    for item in collection:
        all_cryptocurrencies.append(CryptoCurrency(**item))
    if not all_cryptocurrencies:
        raise HTTPException(status_code=404, detail="No items found")
    return all_cryptocurrencies


@app.post('/api/cryptocurrency')
async def insert_cryptocurrency(crypto_currency: CryptoCurrency):
    crypto_data = crypto_currency.dict()
    result = database.insert_cryptocurrency(crypto_data)
    if result:
        return {"message": "Cryptocurrency created successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to create cryptocurrency")


@app.get('/api/test')
async def test_endpoint():
    return {"message": "FastAPI is working!"}


# Run the application if this script is executed directly
# RUN THIS IN TERMINAL: uvicorn crypto_api.routes:app --host 127.0.0.1 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)