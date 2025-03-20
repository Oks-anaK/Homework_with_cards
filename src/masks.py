import logging

path_to_log = 'C:\\Users\\Oks-py\\PycharmProjects\\PythonProject6\\logs\\masks.log'

logger = logging.getLogger('masks')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(path_to_log, encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def get_mask_card_number(user_number_card: str) -> str:
    """Функция маскирует номер банковской карты в виде: XXXX XX** **** XXXX"""
    logger.info(f'Введен номер карты.')

    number_card = user_number_card.replace(" ", "")

    if not isinstance(number_card, str):
        logger.error("Введен неверный тип данных.")
        raise TypeError("Неверный тип данных.")

    if not number_card.isdigit():
        logger.error("Номер карты содержит недопустимые символы.")
        raise ValueError("Номер карты содержит недопустимые символы.")

    if len(number_card) < 13 or len(number_card) > 19:
        logger.error("Неверная длина номера карты. Допустимая длина: 13-19 символов, "f"а введено: {len(number_card)}.")
        raise ValueError(
            f"Неверная длина номера карты. Допустимая длина: 13-19 символов, а введено: {len(number_card)}."
        )

    logger.info(f'Номер карты замаскирован.')

    return f"{number_card[-19:-12]} {number_card[-12:-10]}** **** {number_card[-4:]}"



def get_mask_account(number_account: str) -> str:
    """Функция маскирует номер счета в виде: **XXXX"""

    logger.info(f'Введен номер cчета.')

    if not isinstance(number_account, str):
        logger.error("Введен неверный тип данных.")
        raise TypeError("Неверный тип данных.")

    if not number_account.isdigit():
        logger.error("Номер счета содержит недопустимые символы.")
        raise ValueError("Номер счета содержит недопустимые символы.")

    if len(number_account) != 20:
        logger.error("Неверная длина номера счета. Должно быть 20 символов.")
        raise ValueError("Неверная длина номера счета. Должно быть 20 символов.")
    logger.info(f'Номер cчета замаскирован.')
    return f"**{number_account[-4:]}"


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
    # print(get_mask_card_number("598685864899a"))
    print(get_mask_account("7365410843013587430"))
