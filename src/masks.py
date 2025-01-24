def mask_account_card(account_card: str) -> str:
    """
    Функция маскирует номер банковской карты в виде: Visa Platinum  XXXX XX** **** XXXX
    """
    if "Счет" in account_card:
        return f"Счет **{account_card[-4:]}"
    else:
        return f"{account_card[0:-17]} {account_card[-16:-12]} {account_card[-12:-10]}** **** {account_card[-4:]}"


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
