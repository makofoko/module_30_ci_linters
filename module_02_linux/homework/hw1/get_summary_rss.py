import os
from typing import Union


def get_summary_rss(file_path: str) -> str:
    """
    Считывает файл с результатом команды `ps aux`,
    суммирует значения из столбца RSS и возвращает
    результат в человекочитаемом формате.

    :param file_path: Путь к файлу с результатом ps aux.
    :return: Строка с суммарным объёмом памяти (Б, Кб, Мб, Гб...).
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл '{file_path}' не найден.")

    total_rss = 0
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]
        for line in lines:
            columns = line.split()
            if len(columns) > 5:
                try:
                    rss_value = int(columns[5])
                    total_rss += rss_value
                except ValueError:
                    continue

    return convert_bytes(total_rss)


def convert_bytes(size_in_bytes: int) -> str:
    """
    Переводит байты в человекочитаемый формат (Б, Кб, Мб, Гб, Тб...).

    :param size_in_bytes: Размер в байтах.
    :return: Строка с размером в удобной единице измерения.
    """
    units = ["Б", "Кб", "Мб", "Гб", "Тб", "Пб"]
    size = float(size_in_bytes)
    unit_index = 0

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{int(size)} {units[unit_index]}"


def main() -> None:
    """
    Основная функция: задаёт путь к файлу и выводит суммарный объём памяти.
    """
    file_path = "output_file.txt"
    try:
        summary = get_summary_rss(file_path)
        print(f"Суммарный объём потребляемой памяти: {summary}")
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    main()
