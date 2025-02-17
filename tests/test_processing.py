from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, result",
    [
        (
            "EXECUTED",
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            "CANCELED",
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
        ("", []),
        ("OTHER_STATE", []),
    ],
)
def test_filter_by_state_normal(trans_date: list[dict], state: str, result: list[dict]) -> None:
    """Проверяет фильтрацию по состоянию для обычных случаев."""
    assert filter_by_state(trans_date, state) == result


def test_filter_by_state_normal_empty_list() -> None:
    """Проверяет фильтрацию по состоянию для пустого списка."""
    assert filter_by_state([]) == []


@pytest.mark.parametrize(
    "another_list, exception",
    [
        ("str", TypeError),
        (537, TypeError),
        ((), TypeError),
        ({}, TypeError),
        (9.8, TypeError),
    ],
)
def test_filter_by_state_negative_type(another_list: Any, exception: type) -> None:
    """Проверяет, что функция вызывает TypeError при некорректном типе входных данных."""
    with pytest.raises(exception):
        filter_by_state(another_list)


@pytest.mark.parametrize(
    "list_not_key_state, exception",
    [
        ([{"id": 41428829, "st": "EXECUTED", "data": "2019-07-03T18:35:29.512364"}], KeyError),
    ],
)
def test_filter_by_state_negative_not_key_state(list_not_key_state: Any, exception: type) -> None:
    """Проверяет, что функция вызывает KeyError, если нет ключа 'state'."""
    with pytest.raises(exception):
        filter_by_state(list_not_key_state)


@pytest.mark.parametrize(
    "descending, result",
    [
        (
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
        (
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
    ],
)
def test_sort_by_date_normal_1(trans_date: list[dict], descending: bool, result: list[dict]) -> None:
    """Проверяет сортировку по дате в прямом и обратном порядке."""
    assert sort_by_date(trans_date, descending) == result


def test_sort_by_date_normal_2(same_data_trans: list[dict]) -> None:
    """Проверяет сортировку по дате для данных с одинаковыми датами."""
    assert sort_by_date(same_data_trans) == [
        {"id": 594226727, "state": "EXECUTED", "date": "2016-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2016-09-12T02:08:58.425572"},
    ]


def test_sort_by_date_normal_empty_list() -> None:
    """Проверяет сортировку по дате для пустого списка."""
    assert sort_by_date([]) == []


@pytest.mark.parametrize(
    "dict_not_key_date, exception",
    [
        ([{"id": 41428829, "state": "EXECUTED", "book": "2019-07-03T18:35:29.512364"}], KeyError),
    ],
)
def test_sort_by_date_negative_not_key_date(dict_not_key_date: Any, exception: type) -> None:
    """Проверяет, что функция вызывает KeyError, если нет ключа 'date'."""
    with pytest.raises(exception):
        sort_by_date(dict_not_key_date)


@pytest.mark.parametrize(
    "date, exception",
    [
        ("str", TypeError),
        (537, TypeError),
        ((), TypeError),
        ({}, TypeError),
        (9.8, TypeError),
    ],
)
def test_sort_by_date_negative_type(date: Any, exception: type) -> None:
    """Проверяет, что функция вызывает TypeError при некорректном типе входных данных."""
    with pytest.raises(exception):
        sort_by_date(date)
