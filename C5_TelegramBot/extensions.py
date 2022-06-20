import requests
import json
from config import currencies, url, API_key_access


class ConvertException(Exception):
    pass


class CurrencyConvertor:
    @staticmethod
    def get_price(base: str, sym: str, amount: str):
        try:
            base_ticker = currencies[base.lower()]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту: {base}')

        try:
            sym_ticker = currencies[sym.lower()]
        except KeyError:
            raise ConvertException(f'Не удалось обработать валюту: {sym}')

        if base_ticker == sym_ticker:
            raise ConvertException(f'Нельзя переводить одинаковые валюты: {base}')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConvertException(f"Не удалось обработать количество: {amount}")

        r = requests.get(f'{url}?fsym={base_ticker}&tsyms={sym_ticker}&api_key={API_key_access}')
        resp = json.loads(r.content)
        total_base = resp[sym_ticker] * amount
        total_base = round(total_base, 2)

        return total_base
