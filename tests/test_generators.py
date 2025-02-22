import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.mark.parametrize(
    "key, result",
    [
        (
            "руб.",
            {
                "id": 873106923,
                "state": "EXECUTED",
                "date": "2019-03-23T01:09:46.296404",
                "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
                "description": "Перевод со счета на счет",
                "from": "Счет 44812258784861134719",
                "to": "Счет 74489636417521191160",
            },
        ),
    ],
)
def test_filter_by_currency(new_trans_list, key, result):
    """Тестирует обычные случаи вывода транзакций по ключу."""
    gen1 = filter_by_currency(new_trans_list, key)
    assert next(gen1) == result


@pytest.mark.parametrize("key, result", [(890, TypeError)])
def test_filter_by_currency_negative_type_key(new_trans_list, key, result):
    """Тестирует случаи, когда тип ввода для ключа не корректен."""
    gen_neg1 = filter_by_currency(new_trans_list, key)
    with pytest.raises(TypeError):
        assert next(gen_neg1) == result


def test_filter_by_currency_negative_type_lst():
    """Тестирует случаи, когда тип ввода lst не корректен."""
    gen_neg3 = filter_by_currency("str", "USD")
    with pytest.raises(TypeError):
        assert next(gen_neg3) == TypeError


@pytest.mark.parametrize("lst, key, result", [([534, 394, "riowur"], "USD", TypeError)])
def test_filter_by_currency_negative_type_dct_in_lst(lst, key, result):
    """Тестирует случаи, когда внутри списка не словарь."""
    gen_neg4 = filter_by_currency(lst, key)
    with pytest.raises(TypeError):
        assert next(gen_neg4) == result


def test_filter_by_currency_missing_key():
    """Тестирует случаи, когда не найдены нужные ключи или тип данных внутри словаря не верен."""
    data = [{}]
    with pytest.raises(ValueError):
        list(filter_by_currency(data, "USD"))


def test_transaction_descriptions(new_trans_list):
    """Тестирует обычные случаи вывода описания транзакций."""
    gen2 = transaction_descriptions(new_trans_list)
    assert next(gen2) == "Перевод организации"


def test_transaction_descriptions_negative_type_lst():
    """Тестирует случаи, когда тип ввода lst не корректен."""
    gen_neg2_1 = transaction_descriptions(684)
    with pytest.raises(TypeError):
        assert next(gen_neg2_1) == TypeError


@pytest.mark.parametrize("lst, result", [([534, 394, "riowur"], TypeError)])
def test_transaction_descriptions_negative_type_dct_in_lst(lst, result):
    """Тестирует случаи, когда внутри списка не словарь."""
    gen_neg2_2 = transaction_descriptions(lst)
    with pytest.raises(TypeError):
        assert next(gen_neg2_2) == result


@pytest.mark.parametrize(
    "lst, result",
    [
        (
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {"amount": "9824.07", "currency": {"name": "U", "code": "U"}},
                    "descript": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "U", "code": "U"}},
                    "descript": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
            ],
            KeyError,
        ),
    ],
)
def test_transaction_descriptions_negative_type_keyerror(lst, result):
    """Тестирует случаи, когда нет ключа description."""
    gen_neg2_3 = transaction_descriptions(lst)
    with pytest.raises(KeyError):
        assert next(gen_neg2_3) == result


@pytest.mark.parametrize(
    "start, stop, result",
    [
        (1, 5, "0000 0000 0000 0001"),
    ],
)
def test_card_number_generator(start, stop, result):
    """Тестирует обычные случаи генерации номеров карт."""
    gen3 = card_number_generator(start, stop)
    assert next(gen3) == result


def test_card_number_generator_negative_type_start():
    """Тестирует случаи, когда в start введен неправильный тип данных."""
    gen_neg3_1 = card_number_generator("str", 6)
    with pytest.raises(TypeError):
        assert next(gen_neg3_1) == TypeError


def test_card_number_generator_negative_type_stop():
    """Тестирует случаи, когда в stop введен неправильный тип данных."""
    gen_neg3_2 = card_number_generator(6, "str")
    with pytest.raises(TypeError):
        assert next(gen_neg3_2) == TypeError
