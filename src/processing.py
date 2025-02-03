def filter_by_state(transactions: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Функция, которая принимает список словарей и опционально значение
    для ключа state (по умолчанию 'EXECUTED'). Функция возвращает новый список словарей,
    содержащий только те словари, у которых ключ state соответствует указанному значению.
    """
    return [transaction for transaction in transactions if transaction["state"] == state]


def sort_by_date(transactions: list[dict], my_reverse: bool = True) -> list[dict]:
    """
    Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция должна возвращать новый список, отсортированный по дате (date).
    """
    sorted_data = sorted(transactions, key=lambda transaction: transaction["date"], reverse=my_reverse)
    return sorted_data


if __name__ == "__main__":
    transactions = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    print(filter_by_state(transactions))
    print(sort_by_date(transactions))
    print(sort_by_date(transactions, my_reverse=False))
