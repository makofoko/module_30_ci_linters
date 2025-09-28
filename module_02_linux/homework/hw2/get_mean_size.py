import sys


def get_mean_size(lines: list[str]) -> float:
    """
    Функция принимает список строк из вывода команды `ls -l`
    и возвращает средний размер файла в байтах.

    :param lines: Список строк (результат выполнения `ls -l`).
    :return: Средний размер файлов (в байтах). Если файлов нет — 0.
    """
    total_size = 0
    file_count = 0

    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 5:
            continue
        try:
            size = int(parts[4])  
            total_size += size
            file_count += 1
        except ValueError:
            continue

    if file_count == 0:
        return 0.0
    return total_size / file_count


def main() -> None:
    """
    Основная функция: читает данные из stdin и выводит средний размер файлов.
    """
    lines = sys.stdin.readlines()
    mean_size = get_mean_size(lines)

    if mean_size == 0:
        print("В каталоге нет файлов или не удалось определить их размер.")
    else:
        print(f"Средний размер файла: {mean_size:.2f} Б")


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
