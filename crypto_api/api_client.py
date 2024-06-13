import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from dotenv import load_dotenv
import os

# Specify the path to the .env file relative to script
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'env', '.env')

# Load environment variables from the specified file
load_dotenv(dotenv_path)
api_key = os.getenv('API_KEY')


class CoinGeckoClient:
    BASE_URL = 'https://api.coingecko.com/api/v3'

    def __init__(self):
        self.session = requests.session()

    def _make_request(self, endpoint, params=None):
        try:
            response = self.session.get(f'{self.BASE_URL}/{endpoint}', params=params)
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            raise
        except ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
            raise
        except Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')
            raise
        except RequestException as req_err:
            print(f'An error occurred: {req_err}')
            raise

    def get_cryptocurrencies(self, vs_currency='usd', order='market_cap_desc', per_page=100, page=1, sparkline=False):
        params = {
            'vs_currency': vs_currency,
            'order': order,
            'per_page': per_page,
            'page': page,
            'sparkline': str(sparkline).lower()
        }
        return self._make_request('coins/markets', params=params)

    def get_historical_data(self, coin_id, date):
        endpoint = f'coins/{coin_id}/history'
        params = {'date': date}
        return self._make_request(endpoint, params=params)

    def get_market_data(self):
        endpoint = 'global'
        return self._make_request(endpoint=endpoint)

    def get_coin_info(self, coin_id):
        endpoint = f'coin/{coin_id}'
        return self._make_request(endpoint)


    # Add more methods as needed for different API endpoints


# Example Usage
if __name__ == "__main__":
    client = CoinGeckoClient()
    try:
        cryptocurrencies = client.get_cryptocurrencies(sparkline=True)
        print(cryptocurrencies)
    except Exception as e:
        print(f'Error fetching cryptocurrencies: {e}')
