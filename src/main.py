import os

from src.analysis import search_by_string_in_operations
from src.generators import filter_by_currency
from src.processing import filter_by_state, sort_by_date
from src.tables import reading_from_csv, reading_from_excel
from src.utils import get_operations
from src.widget import get_date, mask_account_card


def main():
    """Функция, отвечающая за основную логику проекта."""

    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями."
        "\nВыберите необходимый пункт меню:"
        "\n1. Получить информацию о транзакциях из JSON-файла"
        "\n2. Получить информацию о транзакциях из CSV-файла"
        "\n3. Получить информацию о транзакциях из XLSX-файла"
    )

    user_file_format = int(input())
    while user_file_format not in [1, 2, 3]:
        user_file_format = int(input())

    operations = [
        "Для обработки выбран JSON-файл.",
        "Для обработки выбран CSV-файл.",
        "Для обработки выбран XLSX-файл.",
    ]
    choice_format = operations[user_file_format - 1]
    print(choice_format)

    # Проверка существования файлов
    path_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    list_path_form = {
        1: os.path.join("data", "operations.json"),
        2: os.path.join("tables", "transactions.csv"),
        3: os.path.join("tables", "transactions_excel.xlsx"),
    }
    path_form = list_path_form[user_file_format]
    path_to_file = os.path.join(path_base, path_form)

    if not os.path.exists(path_to_file):
        print(f"Ошибка: файл {path_to_file} не найден.")
        return

    # Чтение файла
    read_functions = {
        1: get_operations,
        2: reading_from_csv,
        3: reading_from_excel,
    }
    try:
        read_file = read_functions[user_file_format](path_to_file)
        if not read_file:
            print("Ошибка: файл пуст или имеет неверный формат.")
            return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    # Фильтрация по статусу
    print(
        "Введите статус, по которому необходимо выполнить фильтрацию."
        "\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
    )
    user_status_for_filter = input().upper()
    while user_status_for_filter not in ["EXECUTED", "CANCELED", "PENDING"]:
        user_status_for_filter = input().upper()

    try:
        list_trans_status = filter_by_state(read_file, user_status_for_filter)
        # if not list_trans_status:
        #     print(f"Не найдено транзакций со статусом {user_status_for_filter}")

        print(f"Операции отфильтрованы по статусу {user_status_for_filter}")

        # Сортировка по дате
        print("Отсортировать операции по дате? Да/Нет")
        user_filter_by_date = input().lower()
        while user_filter_by_date not in ["да", "нет"]:
            print(f"Команда {user_filter_by_date} недоступна.\n" "Введите команду: Да или Нет")
            user_filter_by_date = input().lower()

        list_trans_sort_date = list_trans_status
        if user_filter_by_date == "да":
            print("Отсортировать по возрастанию или по убыванию?")
            user_sort_choice = input().lower()
            while user_sort_choice not in ["по возрастанию", "по убыванию"]:
                print(
                    f"Команда {user_sort_choice} недоступна.\n"
                    "Введите параметр сортировки: по возрастанию или по убыванию"
                )
                user_sort_choice = input().lower()
            try:
                if user_sort_choice == "по возрастанию":
                    list_trans_sort_date = sort_by_date(list_trans_status, ascending=True)
                elif user_sort_choice == "по убыванию":
                    list_trans_sort_date = sort_by_date(list_trans_status)
            except Exception as e:
                print(f"Ошибка при сортировке: {e}")
                list_trans_sort_date = list_trans_status  # Используем несортированный список в случае ошибки

        # Фильтрация по валюте
        print("Выводить только рублевые транзакции? Да/Нет")
        user_sort_by_rub = input().lower()
        while user_sort_by_rub not in ["да", "нет"]:
            print(f"Команда {user_sort_by_rub} недоступна.\n" "Введите команду: Да или Нет")
            user_sort_by_rub = input().lower()

        list_of_rub_trans = list_trans_sort_date

        if user_sort_by_rub == "да":
            try:
                if user_file_format == 1:
                    rub_transactions = filter_by_currency(list_of_rub_trans, "руб.")  # Используем 'руб.' для JSON
                elif user_file_format == 2 or user_file_format == 3:
                    rub_transactions = filter_by_currency(
                        list_of_rub_trans, "Ruble"
                    )  # Используем 'Ruble' для CSV и XLSX
                list_of_rub_trans = list(rub_transactions)  # Преобразуем генератор в список
            except Exception as e:
                print(f"Ошибка при фильтрации по валюте: {e}")
                list_of_rub_trans = list_trans_sort_date

        # Фильтрация по описанию
        print("Отфильтровать список транзакций по определенному слову\n" "в описании? Да/Нет")
        user_filter_by_desc = input().lower()
        while user_filter_by_desc not in ["да", "нет"]:
            print(f"Команда {user_filter_by_desc} недоступна.\n" "Введите команду: Да или Нет")
            user_filter_by_desc = input().lower()

        list_trans_desc = list_of_rub_trans
        if user_filter_by_desc == "да":
            user_filter_by_desc_word = input("Ведите ключевое слово для фильтрации.")
            try:
                list_trans_desc = search_by_string_in_operations(list_of_rub_trans, user_filter_by_desc_word)
                # if not list_trans_desc:
                #     print(f"Не найдено транзакций с описанием, содержащим '{user_filter_by_desc_word}'.")
            except Exception as e:
                print(f"Ошибка при фильтрации по описанию: {e}")
                list_trans_desc = list_of_rub_trans  # Используем нефильтрованный список в случае ошибки

        # Вывод результатов
        len_trans = len(list_trans_desc)
        if len_trans == 0 or len_trans is None:
            print("Не найдено ни одной транзакции, подходящей под ваши\nусловия фильтрации")
        else:
            print("Распечатываю итоговый список транзакций...")
            print(f"Всего банковских операций в выборке: {len_trans}")
            for i, dct in enumerate(list_trans_desc):
                try:
                    # Инициализируем переменные для каждой транзакции
                    str_of_widget = ""
                    str_sum = ""
                    str_name_currency = ""
                    str_from = ""
                    str_to = ""
                    # Обработка даты
                    if dct.get("date") and isinstance(dct.get("date"), str):
                        try:
                            str_of_widget = get_date(dct.get("date"))
                        except Exception as e:
                            print(f"Ошибка при обработке даты: {e}")
                            str_of_widget = "Дата неизвестна"

                    # Обработка суммы и валюты - проверяем оба возможных формата
                    try:
                        # Формат 1: operationAmount -> amount, currency -> name
                        operation_amount = dct.get("operationAmount")
                        if operation_amount:
                            str_sum = operation_amount.get("amount", "")
                            currency = operation_amount.get("currency")
                            if currency:
                                str_name_currency = currency.get("name", "")
                        # Формат 2: amount, currency_name напрямую в словаре
                        else:
                            str_sum = dct.get("amount", "")
                            str_name_currency = dct.get("currency_name", "")
                    except Exception as e:
                        print(f"Ошибка при обработке суммы и валюты: {e}")
                        str_sum = "Сумма неизвестна"
                        str_name_currency = ""

                    # Обработка счетов отправителя и получателя
                    try:
                        if dct.get("to") and isinstance(dct.get("to"), str):
                            str_to = mask_account_card(dct.get("to"))
                        else:
                            str_to = "Счет получателя не указан"
                    except Exception as e:
                        print(f"Ошибка при обработке счета получателя: {e}")
                        str_to = "Счет получателя не удалось обработать"

                    try:
                        if dct.get("from") and isinstance(dct.get("from"), str):
                            str_from = mask_account_card(dct.get("from"))
                        else:
                            str_from = "Счет отправителя не указан"
                    except Exception as e:
                        print(f"Ошибка при обработке счета отправителя: {e}")
                        str_from = "Счет отправителя не удалось обработать"

                    # Вывод информации о транзакции
                    if dct.get("description"):
                        desc_transaction = dct.get("description")
                        if dct.get("from") and isinstance(dct.get("from"), str):
                            print(
                                f"{str_of_widget} {desc_transaction}\n{str_from} -> {str_to}\n"
                                f"Сумма: {str_sum} {str_name_currency}"
                            )
                        else:
                            print(
                                f"{str_of_widget} {desc_transaction}\n{str_to}\n"
                                f"Сумма: {str_sum} {str_name_currency}"
                            )
                    else:
                        print(f"{str_of_widget} Описание отсутствует\n{str_to}\nСумма: {str_sum} {str_name_currency}")
                except Exception as e:
                    print(f"Ошибка при обработке транзакции {i + 1}: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


# if __name__ == "__main__":
#     main()
