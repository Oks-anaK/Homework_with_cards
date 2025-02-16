from curses.ascii import isdigit


def get_mask_card_number(number_card: str) -> str:
    """Функция маскирует номер банковской карты в виде: XXXX XX** **** XXXX"""
    if not isinstance(number_card, str):
        raise TypeError("Неверный тип данных.")
    if not number_card.isdigit():
        raise ValueError("Номер карты содержит недопустимые символы.")
    if len(number_card) < 13 or len(number_card) > 19:
        raise ValueError(
            f"Неверная длина номера карты. Допустимая длина: 13-19 символов, а введено: {len(number_card)}"
        )
    return f"{number_card[-19:-12]} {number_card[-12:-10]}** **** {number_card[-4:]}"


def get_mask_account(number_account: str) -> str:
    """Функция маскирует номер счета в виде: **XXXX"""
    if not isinstance(number_account, str):
        raise TypeError("Неверный тип данных.")
    if not number_account.isdigit():
        raise ValueError("Номер счета содержит недопустимые символы.")
    if len(number_account) != 20:
        raise ValueError("Неверная длина номера счета. Должно быть 20 символов.")
    return f"**{number_account[-4:]}"


# if __name__ == "__main__":
#     print(get_mask_card_number("7000792289606361"))
#     print(get_mask_account("73654108430135874305"))
#     print(get_mask_card_number("598685864899a"))
