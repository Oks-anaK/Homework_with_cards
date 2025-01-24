def mask_account_card(account_card: str) -> str:
    """
    Функция маскирует номер банковской карты в виде: Visa Platinum  XXXX XX** **** XXXX
    """
    if "Счет" in account_card:
        return f'{account_card[-16:-12]} {account_card[-12:-10]}** **** {account_card[-4:]}'
    else:
        return f'Счет **{account_card[-4:]}'



if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))
