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


def ping_test(endpoints_obj):
    endpoints.ping()

def coin_list_test(endpoints_obj):
    endpoints.set_coins_list()
    print(endpoints.coin_list)

def price_examples_test(endpoints_obj):
    bitcoin_example = endpoints.get_coin_price(['bitcoin'], 'usd', True, True, True, True)
    print(bitcoin_example)
    ethereum_example = endpoints.get_coin_price(['ethereum'], 'usd', True, True, True, True)
    print(ethereum_example)
    two_coins_example = endpoints.get_coin_price(['bitcoin', 'ethereum'], 'usd', True, True, True, True)
    print(two_coins_example)


if __name__ == '__main__':
    endpoints = ENDPOINTS()
    # ping_test(endpoints)
    # coin_list_test(endpoints)
    price_examples_test(endpoints)


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


