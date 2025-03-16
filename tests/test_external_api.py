from unittest.mock import patch

import pytest
import requests

from src.external_api import convert_transaction_amount_to_rubles


@patch("src.external_api.requests.get")
def test_convert_transaction_amount_to_rubles_positive_usd(mock_currency_api, convert_transaction_usd):
    """Проверка с USD."""
    mock_currency_api.return_value.status_code = 200
    mock_currency_api.return_value.json.return_value = {"result": 17080.56}
    expected_result = 17080.56

    assert convert_transaction_amount_to_rubles(convert_transaction_usd) == expected_result
    mock_currency_api.assert_called_once()


def test_convert_transaction_amount_to_rubles_positive_rub(convert_transaction_rub):
    """Проверка с RUB."""
    assert convert_transaction_amount_to_rubles(convert_transaction_rub) == 100.0


@patch("src.external_api.requests.get", side_effect=requests.exceptions.HTTPError())
def test_convert_transaction_amount_to_rubles_error_in_requests(mock_currency_api, convert_transaction_usd):
    """Проверка на вызов ошибки HTTPError()."""
    with pytest.raises(requests.exceptions.RequestException, match="Ошибка в работе библиотеки requests."):
        convert_transaction_amount_to_rubles(convert_transaction_usd)


@patch("src.external_api.requests.get")
def test_convert_transaction_amount_to_rubles_no_key_in_api(mock_currency_api, convert_transaction_usd):
    """Проверка на вызов ошибки KeyError для API."""
    mock_currency_api.return_value.status_code = 200
    mock_currency_api.return_value.json.return_value = {}

    with pytest.raises(KeyError, match="Нет ключа 'result' для USD в API."):
        convert_transaction_amount_to_rubles(convert_transaction_usd)


def test_convert_transaction_amount_to_rubles_no_key_in_dict():
    """Проверка на вызов ошибки KeyError в словаре."""
    dict_no_key = {"id": 441945886, "operationAmount": {"amount": "31957.58", "currency": {"another_key": "RUB"}}}

    with pytest.raises(KeyError, match="Ключ в словаре не найден."):
        assert convert_transaction_amount_to_rubles(dict_no_key) == KeyError


def test_convert_transaction_amount_to_rubles_typeerror():
    """Проверка на неправильный тип входных данных."""
    transaction_no_dict = [
        {"id": 441945886, "operationAmount": {"amount": "100", "currency": {"code": "RUB"}}}
    ]
    with pytest.raises(TypeError, match="Неправильный тип входных данных. Ожидается dict."):
        assert convert_transaction_amount_to_rubles(transaction_no_dict) == TypeError
