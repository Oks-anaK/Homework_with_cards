import os
import sys
from io import StringIO
from unittest.mock import patch

import pytest

from src.main import main

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SAMPLE_DATA = [
    {
        "id": "1",
        "state": "EXECUTED",
        "date": "2023-01-01T12:00:00Z",
        "operationAmount": {"amount": "100", "currency": {"code": "RUB", "name": "руб."}},
        "description": "Перевод организации",
        "from": "Счет 12345678901234567890",
        "to": "Счет 09876543210987654321",
    },
    {
        "id": "2",
        "state": "CANCELED",
        "date": "2023-01-02T12:00:00Z",
        "operationAmount": {"amount": "200", "currency": {"code": "USD", "name": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa 1234 5678 9012 3456",
        "to": "MasterCard 6543 2109 8765 4321",
    },
]


@pytest.fixture
def setup_mocks(monkeypatch):
    """Фикстура для мокирования зависимостей функции main."""
    monkeypatch.setattr("src.utils.get_operations", lambda path=None: SAMPLE_DATA)
    monkeypatch.setattr("src.tables.reading_from_csv", lambda path: SAMPLE_DATA)
    monkeypatch.setattr("src.tables.reading_from_excel", lambda path: SAMPLE_DATA)
    monkeypatch.setattr("os.path.exists", lambda path: True)  # Мокаем os.path.exists
    monkeypatch.setattr(
        "src.processing.filter_by_state",
        lambda operations, state: [op for op in operations if op.get("state") == state],
    )
    monkeypatch.setattr(
        "src.processing.sort_by_date",
        lambda operations, ascending=True: sorted(operations, key=lambda x: x.get("date"), reverse=not ascending),
    )

    def mock_filter_by_currency(operations, currency):
        """Мокирует функцию filter_by_currency для возврата операций, соответствующих заданной валюте."""
        return (op for op in operations if op.get("operationAmount", {}).get("currency", {}).get("name") == currency)

    monkeypatch.setattr("src.generators.filter_by_currency", mock_filter_by_currency)
    monkeypatch.setattr(
        "src.analysis.search_by_string_in_operations",
        lambda operations, search_string: [
            op for op in operations if search_string.lower() in op.get("description", "").lower()
        ],
    )
    monkeypatch.setattr("src.widget.get_date", lambda date_str: "01.01.2023")
    monkeypatch.setattr(
        "src.widget.mask_account_card",
        lambda account_str: "Счет **1234" if "Счет" in account_str else "Карта **** 1234",
    )


def test_main_json_file_choice(setup_mocks):
    """Тест выбора JSON файла и успешной фильтрации."""
    with (
        patch("builtins.input", side_effect=["1", "EXECUTED", "нет", "нет", "нет"]),
        patch("sys.stdout", new=StringIO()) as fake_out,
    ):
        main()
        output = fake_out.getvalue()
        assert "Для обработки выбран JSON-файл" in output
        assert "Операции отфильтрованы по статусу EXECUTED" in output


def test_main_csv_file_choice(setup_mocks):
    """Тест выбора CSV файла и успешной фильтрации."""
    with (
        patch("builtins.input", side_effect=["2", "EXECUTED", "нет", "нет", "нет"]),
        patch("sys.stdout", new=StringIO()) as fake_out,
    ):
        main()
        output = fake_out.getvalue()
        assert "Для обработки выбран CSV-файл" in output
        assert "Операции отфильтрованы по статусу EXECUTED" in output


def test_main_xlsx_file_choice(setup_mocks):
    """Тест выбора XLSX файла и успешной фильтрации."""
    with (
        patch("builtins.input", side_effect=["3", "EXECUTED", "нет", "нет", "нет"]),
        patch("sys.stdout", new=StringIO()) as fake_out,
    ):
        main()
        output = fake_out.getvalue()
        assert "Для обработки выбран XLSX-файл" in output
        assert "Операции отфильтрованы по статусу EXECUTED" in output


def test_main_filter_by_executed(setup_mocks):
    """Тест фильтрации операций по статусу 'EXECUTED'."""
    with (
        patch("builtins.input", side_effect=["1", "EXECUTED", "нет", "нет", "нет"]),
        patch("sys.stdout", new=StringIO()) as fake_out,
    ):
        main()
        output = fake_out.getvalue()
        assert "Операции отфильтрованы по статусу EXECUTED" in output


def test_main_filter_by_canceled(setup_mocks):
    """Тест фильтрации операций по статусу 'CANCELED'."""
    with (
        patch("builtins.input", side_effect=["1", "CANCELED", "нет", "нет", "нет"]),
        patch("sys.stdout", new=StringIO()) as fake_out,
    ):
        main()
        output = fake_out.getvalue()
        assert "Операции отфильтрованы по статусу CANCELED" in output


def test_main_sort_by_date_ascending(setup_mocks):
    """Тест сортировки операций по дате в порядке возрастания."""
    with (
        patch("builtins.input", side_effect=["1", "EXECUTED", "да", "по возрастанию", "нет", "нет"]),
        patch("sys.stdout", new=StringIO()) as fake_out,
    ):
        main()
        output = fake_out.getvalue()
        assert "Операции отфильтрованы по статусу EXECUTED" in output
        assert "Отсортировать операции по дате?" in output
        assert "Отсортировать по возрастанию или по убыванию?" in output


def test_main_sort_by_date_descending(setup_mocks):
    """Тест сортировки операций по дате в порядке убывания."""
    with (
        patch("builtins.input", side_effect=["1", "EXECUTED", "да", "по убыванию", "нет", "нет"]),
        patch("sys.stdout", new=StringIO()) as fake_out,
    ):
        main()
        output = fake_out.getvalue()
        assert "Операции отфильтрованы по статусу EXECUTED" in output
        assert "Отсортировать операции по дате?" in output
        assert "Отсортировать по возрастанию или по убыванию?" in output


def test_main_filter_by_currency_rub(setup_mocks):
    """Тест фильтрации операций по валюте (рубли)."""
    with (
        patch("builtins.input", side_effect=["1", "EXECUTED", "нет", "да", "нет"]),
        patch("sys.stdout", new=StringIO()) as fake_out,
    ):
        main()
        output = fake_out.getvalue()
        assert "Операции отфильтрованы по статусу EXECUTED" in output
        assert "Выводить только рублевые транзакции?" in output
        assert "Всего банковских операций в выборке:" in output


def test_main_filter_by_description(setup_mocks):
    """Тест фильтрации операций по описанию."""
    with (
        patch("builtins.input", side_effect=["1", "EXECUTED", "нет", "нет", "да", "Перевод"]),
        patch("sys.stdout", new=StringIO()) as fake_out,
    ):
        main()
        output = fake_out.getvalue()
        assert "Операции отфильтрованы по статусу EXECUTED" in output
        assert "Отфильтровать список транзакций по определенному слову" in output
        assert "Всего банковских операций в выборке:" in output


def test_main_file_read_error(monkeypatch):
    """Тест обработки ошибки чтения файла."""

    def mock_get_operations_error(*args, **kwargs):
        """Мокируем get_operations для эмуляции ошибки чтения файла."""
        raise Exception("Ошибка чтения файла")

    monkeypatch.setattr("src.utils.get_operations", mock_get_operations_error)
    monkeypatch.setattr("os.path.exists", lambda path: True)

    with patch("builtins.input", side_effect=["1", "EXECUTED"]), patch("sys.stdout", new=StringIO()) as fake_out:
        main()
        output = fake_out.getvalue()
        assert "Произошла непредвиденная ошибка:" in output


def test_main_empty_filter_result(setup_mocks, monkeypatch):
    """Тест для случая, когда после всех фильтров результат пустой."""

    def mock_filter_by_state_empty(operations, state):
        """Мокируем filter_by_state, чтобы вернуть все операции."""
        return SAMPLE_DATA  # Возвращаем все операции

    def mock_search_by_string_in_operations_empty(operations, search_string):
        """Мокируем search_by_string_in_operations, чтобы вернуть пустой список."""
        return []

    monkeypatch.setattr("src.processing.filter_by_state", mock_filter_by_state_empty)
    monkeypatch.setattr(
        "src.analysis.search_by_string_in_operations", mock_search_by_string_in_operations_empty
    )  # Мокируем search_by_string_in_operations
    monkeypatch.setattr(
        "src.generators.filter_by_currency", lambda operations, currency: operations
    )  # Возвращаем operations без изменений

    with (
        patch("builtins.input", side_effect=["1", "EXECUTED", "нет", "нет", "да", "abc"]),
        patch("sys.stdout", new=StringIO()) as fake_out,
    ):
        main()
        output = fake_out.getvalue()
        assert "Не найдено ни одной транзакции, подходящей под ваши\nусловия фильтрации" in output
