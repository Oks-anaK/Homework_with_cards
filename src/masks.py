def get_mask_card_number(number_card: str) -> str:
    """Функция маскирует номер банковской карты в виде: XXXX XX** **** XXXX"""
    return f"{number_card[:4]} {number_card[4:6]}** **** {number_card[13:]}"


def get_mask_account(number_account: str) -> str:
    """Функция маскирует номер счета в виде: **XXXX"""
    return f"**{number_account[-4:]}"


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
