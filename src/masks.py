import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logger_masks = logging.getLogger("masks")
logger_masks.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(BASE_DIR, "logs", "masks.log"), mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger_masks.addHandler(file_handler)


def get_mask_card_number(user_number_card: str) -> str:
    """Функция маскирует номер банковской карты в виде: XXXX XX** **** XXXX"""
    logger_masks.info("Введен номер карты.")

    # Сначала проверяем тип данных
    if not isinstance(user_number_card, str):
        logger_masks.error("TypeError: Введен неверный тип данных.")
        raise TypeError("Неверный тип данных.")

    # Теперь безопасно можем использовать методы строк
    number_card = user_number_card.replace(" ", "")

    if not number_card.isdigit():
        logger_masks.error("ValueError: Номер карты содержит недопустимые символы.")
        raise ValueError("Номер карты содержит недопустимые символы.")

    if len(number_card) < 13 or len(number_card) > 19:
        logger_masks.error(
            "ValueError: Неверная длина номера карты. Допустимая длина: 13-19 символов, "
            f"а введено: {len(number_card)}."
        )
        raise ValueError(
            f"Неверная длина номера карты. Допустимая длина: 13-19 символов, а введено: {len(number_card)}."
        )

    logger_masks.info("Номер карты замаскирован.")
    return f"{number_card[-19:-12]} {number_card[-12:-10]}** **** {number_card[-4:]}"


def get_mask_account(number_account: str) -> str:
    """Функция маскирует номер счета в виде: **XXXX"""

    logger_masks.info("Введен номер cчета.")

    if not isinstance(number_account, str):
        logger_masks.error("TypeError: Введен неверный тип данных.")
        raise TypeError("Неверный тип данных.")

    if not number_account.isdigit():
        logger_masks.error("ValueError: Номер счета содержит недопустимые символы.")
        raise ValueError("Номер счета содержит недопустимые символы.")

    if len(number_account) != 20:
        logger_masks.error("ValueError: Неверная длина номера счета. Должно быть 20 символов.")
        raise ValueError("Неверная длина номера счета. Должно быть 20 символов.")
    logger_masks.info("Номер cчета замаскирован.")
    return f"**{number_account[-4:]}"


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))
    print(get_mask_account("73654108430135874305"))
    # print(get_mask_card_number("598685864899a"))
    # print(get_mask_account("7365410843013587430"))
