import json
from pathlib import Path


def get_operations(path_to_file: str) -> list:
    """Функция, которая принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых транзакциях."""
    try:
        file_path = Path(path_to_file)
        if not file_path.is_file() or file_path.stat().st_size == 0:
            return []  # Если файл по заданному пути не найден или если файл пуст

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            return []  # Если не list в файле

        return data

    except json.JSONDecodeError:
        return []  # Ошибка json


# if __name__ == "__main__":
#     print(get_operations("C:\\Users\\Oks-py\\PycharmProjects\\PythonProject6\\data\\operations.json"))
# print(get_operations("C:\\Users\\Oks-py\\PycharmProjects\\PythonProject6\\data\\data.json"))
