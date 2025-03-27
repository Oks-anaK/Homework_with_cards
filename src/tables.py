import csv
import os
from pprint import pprint

import pandas as pd


def reading_from_csv(path_to_csv: str) -> list:
    """Функция для считывания финансовых операций из CSV принимает путь к файлу CSV и выдает
    список словарей с транзакциями."""
    if not isinstance(path_to_csv, str):
        raise TypeError("Путь к файлу должен быть строкой.")
    if not path_to_csv:
        raise ValueError("Путь к файлу не может быть пустым.")
    if not os.path.isfile(path_to_csv):
        raise FileNotFoundError(f"Файл не найден по пути: {path_to_csv}.")
    if os.path.getsize(path_to_csv) == 0:
        raise ValueError(f"Файл {path_to_csv} пуст.")
    if not path_to_csv.lower().endswith(".csv"):
        raise ValueError(f"Файл {path_to_csv} не является CSV-файлом.")

    try:
        with open(path_to_csv, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")

            return list(row for row in reader)
    except csv.Error:
        raise csv.Error("Ошибка формата CSV.")


def reading_from_excel(path_to_excel: str) -> list:
    """Функция для считывания финансовых операций из Excel принимает путь к файлу Excel и выдает
    список словарей с транзакциями."""
    if not isinstance(path_to_excel, str):
        raise TypeError("Путь к файлу должен быть строкой.")
    if not path_to_excel:
        raise ValueError("Путь к файлу не может быть пустым.")
    if not os.path.isfile(path_to_excel):
        raise FileNotFoundError(f"Файл не найден по пути: {path_to_excel}.")
    if os.path.getsize(path_to_excel) == 0:
        raise ValueError(f"Файл {path_to_excel} пуст.")
    if not path_to_excel.lower().endswith(".xlsx"):
        raise ValueError(f"Файл {path_to_excel} не является excel-файлом.")

    try:
        ex_reader = pd.read_excel(path_to_excel)
        dict_list = ex_reader.to_dict(orient="records")

        return dict_list
    except Exception:
        raise Exception("Невозможно прочитать файл excel.")


# if __name__ == "__main__":
# pprint(reading_from_csv("C:\\Users\\Oks-py\\PycharmProjects\\PythonProject6\\tables\\transactions.csv"))
# pprint(reading_from_excel("C:\\Users\\Oks-py\\PycharmProjects\\PythonProject6\\tables\\transactions_excel.xlsx"))
