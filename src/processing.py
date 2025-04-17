def filter_by_state(operations: list, state: str = "EXECUTED") -> list:
    """
    Функция, которая принимает список словарей и опционально значение
    для ключа state (по умолчанию 'EXECUTED'). Функция возвращает новый список словарей,
    содержащий только те словари, у которых ключ state соответствует указанному значению.
    """
    if not isinstance(operations, list):
        raise TypeError("Операции должны быть представлены в виде списка")

    filtered_operations = []
    for operation in operations:
        if isinstance(operation, dict):
            # Проверяем наличие ключа 'state' в словаре
            if "state" in operation:
                if operation["state"] == state:
                    filtered_operations.append(operation)
            # Если ключа 'state' нет, пропускаем эту операцию

    return filtered_operations


def sort_by_date(transactions: list, ascending: bool = False) -> list:
    """
    Функция, которая принимает список словарей и необязательный параметр,
    задающий порядок сортировки (по умолчанию — убывание).
    Функция должна возвращать новый список, отсортированный по дате (date).
    """
    if not isinstance(transactions, list):
        raise TypeError("Неверный тип данных.")

    # Фильтруем транзакции, оставляя только те, у которых есть ключ 'date'
    valid_transactions = [
        transaction for transaction in transactions if isinstance(transaction, dict) and "date" in transaction
    ]

    # Сортируем транзакции по дате
    return sorted(valid_transactions, key=lambda transaction: transaction["date"], reverse=not ascending)


# if __name__ == "__main__":
#     transactions = [
#         {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
#         {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
#         {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
#         {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
#     ]
# #     print(filter_by_state(transactions))
# #     print(filter_by_state(transactions, "CANCELED"))
# #     print(sort_by_date(transactions))
#     print(sort_by_date(transactions, ascending=False))
#     #print(filter_by_state([
#         #{"id": 41428829, "date": "2019-07-03T18:35:29.512364"},
#         #{"id": 939719570, "date": "2018-06-30T02:08:58.425572"}]))
#     print(filter_by_state([]))
