import requests
import json
from Config import keys


class ConvertionExpetion(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(base: str, quote: str, amount: str):

        if base == quote:
            raise ConvertionExpetion(f'Не удалось перевести одинаковые валюты: {base}-{quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExpetion(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExpetion(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExpetion(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        result = json.loads(r.content)[keys[quote]]
        result *= amount

        return result
