import requests
import json

# Helper functions
def get_depth(obj):
    """
    tested for list of json objects but should be useful for other data structures.
    recursively checks if each obj has a child. save the maximal depth of the object and return it.
    :param obj:
    :return: depth of obj
    """
    depth = 0

    if isinstance(obj, dict):
        for key, value in obj.items():
            temp_depth = get_depth(value)
            if temp_depth > depth:
                depth = temp_depth

    if isinstance(obj, list):
        for item in obj:
            temp_depth = get_depth(item)
            if temp_depth > depth:
                depth = temp_depth
    return depth + 1


def save_json(dictionary, filename):
    """
    Saves the dictionary to a json file
    :param dictionary:
    :param filename:
    :return: None
    """
    json_object = json.dumps(dictionary, indent=4, sort_keys=True)
    with open(filename, 'w') as f:
        f.write(json_object)
    print(f'Saved {filename}')
    return None




# Common end points testing
class ENDPOINTS():
    def __init__(self):
        self.coin_list = None
        self.currency_list = None
        self.coin_categories = None
        self.key = None
        with open('my_api_key') as f:
            self.key = f.read().strip()
            print(f'key: {self.key}')

    def ping(self):
        # End Point 0: Ping, check if we can connect to server with api key
        url = "https://api.coingecko.com/api/v3/ping"
        headers = {
            "accept": "application/json",
            "x-cg-api-key": self.key
        }
        response = requests.get(url, headers=headers)

        print(response.text)

    def fetch_coin_list(self):
        # End point 1: Coin List, query all supported coins with id, name, and symbol

        url = "https://api.coingecko.com/api/v3/coins/list"
        headers = {
            "accept": "application/json",
            "x-cg-api-key": self.key
        }
        response = requests.get(url, headers=headers)
        response_dict = response.json()
        return response_dict

    def set_coins_list(self):
        """
        Sets the coins list for the ENDPOINTS class
        :return:
        """
        self.coin_list = self.fetch_coin_list()
        return None

    def get_coin_price(
            self,
            coin_api_ids,
            currency,
            include_market_cap=False,
            include_24hr_vol=False,
            include24hr_change=False,
            include_last_updated_at=False,
            use_default_precision=True,
            precision='full'
    ):
        """
        EndPOINT function for getting price of coins.
        April 12th 2024: Looks like optional query endpoints do not add additional return values, only return prices.

        :param coin_api_ids: list of strings
        :param currency: string
        :param include_market_cap: boolean
        :param include_24hr_vol: boolean
        :param include24hr_change: boolean
        :param include_last_updated_at: boolean
        :param default_precision: boolean
        :param precision: string
        :return: dict
        """
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_api_ids[0]}"

        # Test if below adds functionality, else remove.
        if len(coin_api_ids) > 1:
            for coin_api_id in coin_api_ids[1:]:
                # TODO change from %2C%20 to %2C
                url += f"%2C%20{coin_api_id}"
        url += f"&vs_currencies={currency}"
        if include_market_cap:
            url += "&market_cap=true"
        if include_24hr_vol:
            url += "&24hr_vol=true"
        if include24hr_change:
            url += "&24hr_change=true"
        if include_last_updated_at:
            url += "&last_updated_at=true"
        if not use_default_precision:
            url += f"&precision={precision}".format(precision=precision)
        # Test if above functionality, else remove.

        print(url)
        headers = {
            "accept": "application/json",
            "x-cg-api-key": self.key
        }
        response = requests.get(url, headers=headers)
        response_dict = response.json()
        return response.text

    def fetch_currencies_list(self):
        url = "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
        headers = {
            "accept": "application/json",
            "x-cg-api-key": self.key
        }
        response = requests.get(url, headers=headers)
        response_dict = response.json()
        return response_dict

    def set_currencies_list(self):
        self.currency_list = self.fetch_currencies_list()
        return None

    def fetch_market_data(self, coin_api_ids=['bitcoin', 'ethereum', 'litecoin'], currency='btc', category=None):
        """

        :param coin_api_ids: list of strings
        :param currency: string
        :param category: string, default to None. If not set to none will prioritize category over coin_api_ids parameter.
        :return:
        """

        url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={currency}&ids="
        url += coin_api_ids[0]
        if len(coin_api_ids) > 1:
            for coin_api_id in coin_api_ids[1:]:
                url += f"%2C{coin_api_id}"

        if category:
            url += f"&category={category}"

        headers = {
            "accept": "application/json",
            "x-cg-api-key": self.key
        }
        response = requests.get(url, headers=headers)
        response_dict = response.json()
        return response_dict

    def fetch_coin_categories(self):
        url = "https://api.coingecko.com/api/v3/coins/categories/list"
        headers = {
            "accept": "application/json",
            "x-cg-api-key": self.key
        }
        response = requests.get(url, headers=headers)
        response_dict = response.json()
        return response_dict

    def set_coin_categories(self):
        self.coin_categories = self.fetch_coin_categories()





# Testing Functions

def ping_test(endpoints_obj):
    endpoints_obj.ping()


def coin_list_test(endpoints_obj):
    endpoints_obj.set_coins_list()
    print(endpoints_obj.coin_list)


def price_examples_test(endpoints_obj):
    bitcoin_example = endpoints_obj.get_coin_price(['bitcoin'], 'usd', True, True, True, True)
    print(bitcoin_example)
    ethereum_example = endpoints_obj.get_coin_price(['ethereum'], 'usd', True, True, True, True)
    print(ethereum_example)
    two_coins_example = endpoints_obj.get_coin_price(['bitcoin', 'ethereum'], 'usd', True, True, True, True)
    print(two_coins_example)


def currency_list_test(endpoints_obj):
    currencies_list = endpoints_obj.fetch_currencies_list()
    print(currencies_list)


def market_data_test_ids(endpoints_obj):
    market_data = endpoints_obj.fetch_market_data(
        coin_api_ids=['bitcoin', 'ethereum', 'litecoin'],
        currency='btc',
        category=None
    )
    print(market_data)
    save_json(market_data, 'market_data_example.json')
    return


def market_data_test_categories(endpoints_obj):
    market_data = endpoints_obj.fetch_market_data(
        currency='btc',
        category="layer-1"
    )
    print(market_data)
    save_json(market_data, 'market_data_category.json')
    return

def coin_categories_test(endpoints_obj):
    categories = endpoints_obj.set_coin_categories()
    print(endpoints_obj.coin_categories)



if __name__ == '__main__':
    endpoints = ENDPOINTS()
    # ping_test(endpoints)
    # coin_list_test(endpoints)
    # price_examples_test(endpoints)
    # currency_list_test(endpoints)
    # market_data_test_ids(endpoints)
    # market_data_test_categories(endpoints)
    coin_categories_test(endpoints)


# if __name__ == '__main__':
#     endpoints = ENDPOINTS()
#     endpoints.ping()
#     endpoints.set_coins_list()
#     # print(endpoints.coin_list)
#     save_json(endpoints.coin_list, 'coins.json')
#     coins_depth = get_depth(endpoints.coin_list)
#     # print(coins_depth)
#     bitcoin_example = endpoints.get_coin_price('bitcoin', 'usd', True, True, True, True)
#     print(bitcoin_example)
#     ethereum_example = endpoints.get_coin_price('ethereum', 'usd', True, True, True, True)
#     print(ethereum_example)


