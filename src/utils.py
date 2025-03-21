import json
import logging
import os
from pathlib import Path

from src.masks import BASE_DIR




def get_operations(path_to_file: str) -> list:
    """Функция, которая принимает на вход путь до JSON-файла
    и возвращает список словарей с данными о финансовых транзакциях."""

    logger_utils = logging.getLogger("utils")
    logger_utils.setLevel(logging.INFO)
    file_handler = logging.FileHandler(os.path.join(BASE_DIR, "logs", "utils.log"), "w", encoding="utf-8")
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger_utils.addHandler(file_handler)

    try:
        logger_utils.info("Получен путь до JSON-файла.")
        file_path = Path(path_to_file)

        if not file_path.is_file() or file_path.stat().st_size == 0:
            logger_utils.warning("Файл по заданному пути не найден или пуст.")
            return []  # Если файл по заданному пути не найден или если файл пуст

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            logger_utils.warning("Файл содержит тип отличный от list.")
            return []  # Если не list в файле

        logger_utils.info("Получен список словарей с данными о финансовых транзакциях.")
        return data

    except json.JSONDecodeError:
        logger_utils.error("JSONDecodeError: Ошибка формата json.")
        return []  # Ошибка json


if __name__ == "__main__":
    print(get_operations("C:\\Users\\Oks-py\\PycharmProjects\\PythonProject6\\data\\operations.json"))
    # print(get_operations("C:\\Users\\Oks-py\\PycharmProjects\\PythonProject6\\data\\data.json"))
