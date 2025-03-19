import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
url = "https://api.apilayer.com/exchangerates_data/convert"
headers = {"apikey": API_KEY}


def convert_transaction_amount_to_rubles(transaction: Dict[str, Any]) -> float:
    """Функция, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных —
    float. Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют
    и конвертации суммы операции в рубли."""
    if not isinstance(transaction, dict):
        raise TypeError("Неправильный тип входных данных. Ожидается dict.")
    try:
        currency_code = transaction["operationAmount"]["currency"]["code"]
        amount = transaction["operationAmount"]["amount"]
    except KeyError:
        raise KeyError("Ключ в словаре не найден.")
    if currency_code in ["USD", "EUR"]:
        payload = {"amount": str(amount), "from": currency_code, "to": "RUB"}
        try:
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise requests.exceptions.RequestException("Ошибка в работе библиотеки requests.")
        try:
            amount_to_rubles = response.json()["result"]
        except KeyError:
            raise KeyError(f"Нет ключа 'result' для {currency_code} в API.")
        return float(amount_to_rubles)
    return float(amount)
