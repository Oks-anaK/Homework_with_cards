from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(_data: str) -> str:
    """
    Функция переиспользует уже существующие функции маскировки из модуля masks
    и возвращает строку с замаскированным номером
    """
    if not isinstance(_data, str):
        raise TypeError("Неверный тип данных.")
    splitted_data = _data.split(" ")
    digits_only = splitted_data[-1]
    name_of_card_or_account = splitted_data[:-1]
    if _data.isdigit() is True:
        if len(_data) == 20:
            masked_digits_only = get_mask_account(digits_only)
            return masked_digits_only
        else:
            masked_digits_only = get_mask_card_number(digits_only)
            return masked_digits_only
    elif "Счет" in _data:
        masked_digits_only = get_mask_account(digits_only)
    else:
        masked_digits_only = get_mask_card_number(digits_only)
    return " ".join(name_of_card_or_account) + " " + masked_digits_only


def get_date(_date: str) -> str:
    """
    Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ"
    """
    if not isinstance(_date, str):
        raise TypeError("Неверный тип данных.")
    elif not _date:
        return "Пустая строка."

    year = int(_date[0:4])
    month = int(_date[5:7])
    day = int(_date[8:10])

    if not (1 <= month <= 12 and 1 <= day <= 31):  # Проверка числа и месяца
        return "Некорректный ввод."
    # Проверка високосного года (не учитывает все нюансы)
    if month == 2 and day > 29:
        return "Некорректный ввод."
    # Проверка дней в месяцах
    elif month in [4, 6, 9, 11] and day == 31:
        return "Некорректный ввод."
    # `d`:  Вывести число как десятичное.
    #  `02`:  Вывести число с минимальной шириной 2 символа,
    # дополняя слева нулями, если число меньше двух цифр.
    return f"{day:02d}.{month:02d}.{year}"


# if __name__ == "__main__":
# #     print(mask_account_card("Visa Platinum 7000792289606361"))
# #     print(mask_account_card("Счет 73654108430135874305"))
# #     print(get_date("2024-03-11T02:26:18.671407"))
# #     print(mask_account_card("MasterCard 7158300734726758"))
# #     print(mask_account_card("Счет 35383033474447895560"))
# #     print(mask_account_card("Maestro 1596837868705199"))
# #     print(mask_account_card("485395894859485948"))
# #     print(mask_account_card("53894584093049688999"))
# #     print(mask_account_card(""))
#     print(get_date("2019-11-13T17:38:04.800051"))
#     print(get_date("2000.02.30"))
