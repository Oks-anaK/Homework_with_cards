from typing import Any

import pytest

from src.masks import get_mask_account, get_mask_card_number

valid_account = "12345678901234567890"


@pytest.mark.parametrize(
    "numb_card, expected",
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("7158300734726758", "7158 30** **** 6758"),
        ("6785948537584657842", "6785948 53** **** 7842"),
        ("7158300734726", "7 15** **** 4726"),
    ],
)
def test_mask_card_number_normal(numb_card: str, expected: str) -> None:
    """Тестирует успешное маскирование номера карты."""
    assert get_mask_card_number(numb_card) == expected


@pytest.mark.parametrize(
    "card_number, exception",
    [
        (1234567890123456, TypeError),
        (6.785, TypeError),
        ({}, TypeError),
        ([], TypeError),
        ((), TypeError),
    ],
)
def test_get_mask_card_number_type_typeerror(card_number: Any, exception: type) -> None:
    """Тестирует выброс исключений TypeError."""
    with pytest.raises(exception):
        get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "card_number, exception",
    [
        ("123456789012345a", ValueError),
        ("gpoakvapoegkrpea", ValueError),
        ("#%$$^^*()(*(*)(", ValueError),
    ],
)
def test_get_mask_card_number_type_ValueError(card_number: Any, exception: type) -> None:
    """Тестирует выброс исключений ValueError."""
    with pytest.raises(exception):
        get_mask_card_number(card_number)


@pytest.mark.parametrize("card_number", ["123456789012", "12345678901234567890"])
def test_get_mask_card_number_value_error_length(card_number: str) -> None:
    """Тестирует ValueError при неверной длине номера карты."""
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


@pytest.mark.parametrize(
    "account, expected",
    [
        ("73654108430135874305", "**4305"),
        ("35383033474447895560", "**5560"),
    ],
)
def test_get_mask_account_normal(account: str, expected: str) -> None:
    """Тестирует функцию с валидными номерами счетов."""
    assert get_mask_account(account) == expected


@pytest.mark.parametrize(
    "account, exception",
    [
        (123, TypeError),  # Не строка
        ([], TypeError),
        (9.8, TypeError),
        ({}, TypeError),
        ((), TypeError),
        ("abc", ValueError),  # Не цифры
        (valid_account[:-1], ValueError),  # Неправильная длина
    ],
)
def test_get_mask_account_invalid(account: Any, exception: type) -> None:
    """Тестирует функцию с невалидными номерами счетов."""
    with pytest.raises(exception):
        get_mask_account(account)
