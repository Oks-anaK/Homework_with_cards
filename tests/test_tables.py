import csv
from unittest.mock import MagicMock, mock_open, patch

import pandas as pd
import pytest

from src.tables import reading_from_csv, reading_from_excel


@patch("os.path.isfile")
@patch("os.path.getsize")
@patch("builtins.open", new_callable=mock_open, read_data="header1;header2\nvalue1;value2\nvalue3;value4")
@patch("csv.DictReader")
def test_successful_reading_csv(mock_dictreader, mock_file, mock_getsize, mock_isfile):
    """Проверка на правильный путь и успешное чтение."""
    mock_isfile.return_value = True
    mock_getsize.return_value = 100  # Не пустой файл

    # Настройка DictReader мока: MagicMock — это класс из библиотеки unittest.mock, который создаёт
    # "волшебный" объект-заменитель для любого другого объекта.
    mock_reader = MagicMock()
    # __iter__ — это специальный(магический) метод в Python, который делает объект итерируемым."
    mock_reader.__iter__.return_value = [
        {"header1": "value1", "header2": "value2"},
        {"header1": "value3", "header2": "value4"},
    ]
    mock_dictreader.return_value = mock_reader

    result = reading_from_csv("test.csv")

    mock_isfile.assert_called_once_with("test.csv")
    mock_getsize.assert_called_once_with("test.csv")
    mock_file.assert_called_once_with("test.csv", encoding="utf-8")
    mock_dictreader.assert_called_once()

    assert len(result) == 2
    assert result[0]["header1"] == "value1"
    assert result[1]["header2"] == "value4"


@patch("os.path.isfile")
def test_file_not_found(mock_isfile):
    """Проверка на отсутствие файла."""
    mock_isfile.return_value = False

    with pytest.raises(FileNotFoundError):
        reading_from_csv("none.csv")


def test_empty_path():
    """Проверка на пустой путь."""
    with pytest.raises(ValueError):
        reading_from_csv("")


def test_invalid_path_type():
    """Проверка на неправильный тип пути."""
    with pytest.raises(TypeError):
        reading_from_csv(123)


@patch("os.path.isfile")
@patch("os.path.getsize")
def test_empty_file(mock_getsize, mock_isfile):
    """Проверка на пустой файл."""
    mock_isfile.return_value = True
    mock_getsize.return_value = 0  # Пустой файл

    with pytest.raises(ValueError):
        reading_from_csv("empty.csv")


@patch("os.path.isfile")
@patch("os.path.getsize")
def test_invalid_extension(mock_getsize, mock_isfile):
    """Проверка на неправильное расширение файла."""
    mock_isfile.return_value = True
    mock_getsize.return_value = 100  # Не пустой файл

    with pytest.raises(ValueError):
        reading_from_csv("file.txt")


@patch("os.path.isfile")
@patch("os.path.getsize")
@patch("builtins.open", new_callable=mock_open, read_data="header1;header2\nvalue1;value2")
@patch("csv.DictReader")
def test_csv_error(mock_dictreader, mock_file, mock_getsize, mock_isfile):
    """Проверка на ошибки при чтении CSV."""
    mock_isfile.return_value = True
    mock_getsize.return_value = 100

    mock_dictreader.side_effect = csv.Error("Ошибка формата CSV.")

    with pytest.raises(csv.Error):
        reading_from_csv("test.csv")


@patch("os.path.isfile")
@patch("os.path.getsize")
@patch("pandas.read_excel")
def test_reading_from_excel_successful(mock_read_excel, mock_getsize, mock_isfile):
    """Проверка на правильный путь и успешное чтение excel."""
    mock_isfile.return_value = True
    mock_getsize.return_value = 100

    test_data = [{"header1": "value1", "header2": "value2"}, {"header1": "value3", "header2": "value4"}]
    test_df = pd.DataFrame(test_data)
    mock_read_excel.return_value = test_df

    result = reading_from_excel("test_data.xlsx")

    mock_isfile.assert_called_once_with("test_data.xlsx")
    mock_getsize.assert_called_once_with("test_data.xlsx")
    mock_read_excel.assert_called_once_with("test_data.xlsx")

    assert len(result) == 2
    assert result[0]["header1"] == "value1"
    assert result[1]["header2"] == "value4"


def test_reading_from_excel_empty_path():
    """Проверка на пустой путь."""
    with pytest.raises(ValueError):
        reading_from_excel("")


def test_reading_from_excel_path_typeerror():
    """Проверка на неправильный тип пути."""
    with pytest.raises(TypeError):
        reading_from_excel(569)


@patch("os.path.isfile")
def test_reading_from_excel_file_not_found(mock_isfile):
    """Проверка на отсутствие файла."""
    mock_isfile.return_value = False

    with pytest.raises(FileNotFoundError):
        reading_from_excel("none.xlsx")


@patch("os.path.isfile")
@patch("os.path.getsize")
def test_reading_from_excel_empty_file(mock_getsize, mock_isfile):
    """Проверка на пустой файл."""
    mock_isfile.return_value = True
    mock_getsize.return_value = 0

    with pytest.raises(ValueError):
        reading_from_excel("empty.xlsx")


@patch("os.path.isfile")
@patch("os.path.getsize")
def test_reading_from_excel_invalid_extension(mock_getsize, mock_isfile):
    """Проверка на неправильное расширение файла."""
    mock_isfile.return_value = True
    mock_getsize.return_value = 100

    with pytest.raises(ValueError):
        reading_from_excel("file.txt")


@patch("os.path.getsize")
@patch("os.path.isfile")
@patch("pandas.read_excel")
def test_reading_from_excel_invalid_format(mock_read_excel, mock_isfile, mock_getsize):
    """Проверка на неправильный формат файла excel."""
    mock_isfile.return_value = True
    mock_getsize.return_value = 100

    mock_read_excel.side_effect = Exception("Невозможно прочитать файл excel.")

    with pytest.raises(Exception):
        reading_from_excel("corrupted_file.xlsx")
