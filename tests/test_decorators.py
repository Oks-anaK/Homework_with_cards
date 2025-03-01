import pytest

from src.decorators import log


def test_log_positive():
    """Проверяет как декоратор производит logging в обычных случаях."""

    @log(filename="mylog.txt")
    def perform_summation(x, y):
        return x + y

    perform_summation(1, 3)
    with open("mylog.txt", "r", encoding="utf-8") as f:
        all_str = f.readlines()
        message = all_str[-1]
    assert message == "perform_summation ok\n"


def test_log_error_console_output(capsys):
    """Проверяет, как декоратор обрабатывает случаи с неправильным типом данных"""

    @log()
    def perform_summation(x, y):
        return x + y

    with pytest.raises(TypeError):
        perform_summation(1, "2")

    message = capsys.readouterr()
    assert message.out == "perform_summation error: TypeError. Inputs: (1, '2')\n\n"
