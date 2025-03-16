import json
from unittest.mock import mock_open, patch

from src.utils import get_operations


def test_get_operations_positive() -> None:
    """Проверка обычных случаев."""
    test_data = [{"id": 1, "amount": 100, "currency": "USD"}, {"id": 2, "amount": 200, "currency": "EUR"}]
    # Патчим путь к Path
    with patch("src.utils.Path") as mock_path:
        mock_path.return_value.is_file.return_value = True
        mock_path.return_value.stat.return_value.st_size = 100

        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            result = get_operations("test.json")
            assert result == test_data


@patch("pathlib.Path")
def test_get_operations_file_not_found(mock_path) -> None:
    """Проверка на неправильный путь до файла."""
    # Настраиваем мок, чтобы is_file() возвращал False
    mock_path.return_value.is_file.return_value = False
    result = get_operations("несуществующий_файл.json")

    assert result == []


@patch("pathlib.Path")
@patch("builtins.open")  # builtins - это модуль, содержащий все встроенные функции Python, open() в том числе
def test_get_operations_empty_file(mock_open_func, mock_path) -> None:
    """Проверка пустого файла."""
    # Настраиваем Path.stat() для возврата размера файла 0
    mock_path.return_value.stat.return_value.st_size = 0

    # Настраиваем mock для open().
    # mock_open - это
    # специальная функция из модуля unittest.mock, которая создаёт мок-объект для имитации операций с файлами.
    # read_data - это
    # параметр ф-ии mock_open, который определяет содержимое "файла" при его чтении.
    mock_open_func.return_value = mock_open(read_data="").return_value

    result = get_operations("пустой_файл.json")
    assert result == []


@patch("src.utils.Path")
def test_get_operations_not_list_simplified(mock_path) -> None:
    """Проверка на неправильный тип данных в файле(не list)."""
    mock_path.return_value.is_file.return_value = True
    mock_path.return_value.stat.return_value.st_size = 100

    # Простой словарь в качестве данных
    with patch("builtins.open", mock_open(read_data='{"simple": "dict"}')):
        result = get_operations("test.json")
        assert result == []


@patch("src.utils.Path")
def test_get_operations_invalid_json_simplified(mock_path) -> None:
    """Проверка на неккоректный тип данных для json."""
    mock_path.return_value.is_file.return_value = True
    mock_path.return_value.stat.return_value.st_size = 100

    # Максимально простой некорректный JSON
    with patch("builtins.open", mock_open(read_data="{")):
        result = get_operations("test.json")
        assert result == []


def test_get_operations_empty_list() -> None:
    """Проверка пустого списка в файле."""
    with patch("src.utils.Path") as mock_path:
        mock_path.return_value.is_file.return_value = True
        mock_path.return_value.stat.return_value.st_size = 2

        with patch("builtins.open", mock_open(read_data="[]")):
            result = get_operations("test.json")
            assert result == []


def test_get_operations_nested_data() -> None:
    """Проверка вложенных структур данных."""
    test_data = [
        {"id": 1, "details": {"amount": 100, "currency": "USD"}},
        {"id": 2, "details": {"amount": 200, "currency": "EUR"}},
    ]

    with patch("src.utils.Path") as mock_path:
        mock_path.return_value.is_file.return_value = True
        mock_path.return_value.stat.return_value.st_size = 100

        with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):
            result = get_operations("test.json")
            assert result == test_data
