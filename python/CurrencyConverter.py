# write your code here!
import requests
import json


class CurrencyConv:
    def __init__(self):
        pass

    def get_rates(self, currency_code: str):
        r = requests.get(f"http://www.floatrates.com/daily/{currency_code.lower()}.json")
        result_obj = json.loads(r.text)
        usd = result_obj['usd']
        eur = result_obj['eur']
        print(usd)
        print(eur)


def main():
    converter = CurrencyConv()
    currency_to_convert = input()
    converter.get_rates(currency_to_convert)


if __name__ == '__main__':
    main()
