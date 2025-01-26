from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(_data: str) -> str:
    """
    Функция переиспользует уже существующие функции маскировки из модуля masks
    и возвращает строку с замаскированным номером
    """
    splitted_data = _data.split(" ")
    digits_only = splitted_data[-1]
    name_of_card_or_account = splitted_data[:-1]
    if "Счет" in _data:
        masked_digits_only = get_mask_account(digits_only)
    else:
        masked_digits_only = get_mask_card_number(digits_only)
    return " ".join(name_of_card_or_account) + " " + masked_digits_only


def get_date(_date: str) -> str:
    """
    Функция принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ"
    """
    return f"{_date[8:10]}.{_date[5:7]}.{_date[0:4]}"


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))
    print(mask_account_card("MasterCard 7158300734726758"))
    print(mask_account_card("Счет 35383033474447895560"))
    print(mask_account_card("Maestro 1596837868705199"))
