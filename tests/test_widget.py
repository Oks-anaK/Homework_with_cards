from typing import Any

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "acc_card, result",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("78983698758676", "78 98** **** 8676"),
        ("94385784539485873847", "**3847"),
        ("Счет 73654108467895687615", "Счет **7615"),
    ],
)
def test_mask_account_card_normal(acc_card: str, result: str) -> None:
    """Проверяет маскировку номера и счета для обычных случаев и некорректного ввода."""
    assert mask_account_card(acc_card) == result


@pytest.mark.parametrize(
    "account_card, exception",
    [
        ([], TypeError),
        (537, TypeError),
        ((), TypeError),
        ({}, TypeError),
        (9.8, TypeError),
    ],
)
def test_mask_account_card_negative(account_card: Any, exception: type) -> None:
    """Проверяет, что функция вызывает TypeError при некорректном типе входных данных."""
    with pytest.raises(exception):
        mask_account_card(account_card)


@pytest.mark.parametrize(
    "date_trans, result",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2007-12-12T00:00:00.938259", "12.12.2007"),
        ("", "Пустая строка."),
        ("2005-04-27", "27.04.2005"),
        ("2007/11/02", "02.11.2007"),
        ("2022/13/32", "Некорректный ввод."),
        ("2000.02.30", "Некорректный ввод."),
        ("2003-00-00", "Некорректный ввод."),
        ("2002-06-31", "Некорректный ввод."),
    ],
)
def test_get_date_normal(date_trans: str, result: str) -> None:
    """Проверяет форматирование даты для обычных случаев и некорректного ввода."""
    assert get_date(date_trans) == result


@pytest.mark.parametrize(
    "date_, exception",
    [
        ([], TypeError),
        (537, TypeError),
        ((), TypeError),
        ({}, TypeError),
        (9.8, TypeError),
    ],
)
def test_get_date_negative(date_: Any, exception: type) -> None:
    """Проверяет, что функция вызывает TypeError при некорректном типе входных данных."""
    with pytest.raises(exception):
        get_date(date_)
