import pytest


@pytest.fixture
# Фикстура, которая используется в качестве входных данных для функций:
# test_filter_by_state_normal, test_sort_by_date_normal_1
def trans_date() -> list[dict]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
# Фикстура, которая используется в качестве входных данных для функции:
# test_sort_by_date_normal_2
def same_data_trans() -> list[dict]:
    return [
        {"id": 939719570, "state": "EXECUTED", "date": "2016-09-12T02:08:58.425572"},
        {"id": 594226727, "state": "EXECUTED", "date": "2016-09-12T21:27:25.241689"},
    ]
