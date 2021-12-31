# write your code here!
import requests
import json


class CurrencyConv:
    def __init__(self):
        self.rates = {}
        pass

    def cache_rate(self, currency: str):
        code = currency.lower()
        r = requests.get(f"http://www.floatrates.com/daily/{code}.json")
        result_obj = json.loads(r.text)
        for to_currency in result_obj:
            if to_currency not in self.rates:
                self.rates[to_currency] = {}
            self.rates[to_currency][currency] = result_obj[to_currency]['inverseRate']

    def get_rate(self, from_currency: str, to_currency: str):
        print("Checking the cache...")
        if from_currency in self.rates and to_currency in self.rates[from_currency]:
            print("Oh! It is in the cache!")
            return self.rates[from_currency][to_currency]
        print("Sorry, but it is not in the cache!")
        r = requests.get(f"http://www.floatrates.com/daily/{from_currency.lower()}.json")
        result_obj = json.loads(r.text)
        if from_currency not in self.rates:
            self.rates[from_currency] = {}
        rate = result_obj[to_currency]['rate']
        self.rates[from_currency][to_currency] = rate
        return rate


def main():
    converter = CurrencyConv()
    currencies_to_cache = ('usd', 'eur')
    for currency in currencies_to_cache: # caching usd and eur
        converter.cache_rate(currency)
    from_currency = input().lower()
    while True:
        to_currency = input().lower()
        if to_currency == '':  # End of input
            exit(0)
        to_amount = int(input())
        rate = converter.get_rate(from_currency, to_currency)
        amount = to_amount * rate
        print(f'You received {round(amount, 2)} {to_currency.upper()}.')


if __name__ == '__main__':
    main()
