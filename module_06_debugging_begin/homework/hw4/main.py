import json
import re
import sys
from collections import Counter
from typing import Dict, Iterator, Any

LOG_FILE = 'skillbox_json_messages.log'

def read_logs() -> Iterator[Dict[str, Any]]:
    """
    Вспомогательный генератор.
    Читает LOG_FILE, парсит каждую строку как JSON.
    Пропускает битые строки.
    """
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    if line.strip():
                        yield json.loads(line)
                except json.JSONDecodeError:
                    print(f"Пропуск невалидной JSON-строки: {line.strip()}", file=sys.stderr)
                    continue
    except FileNotFoundError:
        print(f"Критическая ошибка: Файл логов '{LOG_FILE}' не найден.", file=sys.stderr)
        return


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    level_counts = Counter(entry['level'] for entry in read_logs())
    return dict(level_counts)


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час (int)
    """
    hour_counts = Counter()
    for entry in read_logs():
        try:
            hour = int(entry['time'].split(':')[0])
            hour_counts[hour] += 1
        except (ValueError, IndexError, KeyError):
            continue

    if not hour_counts:
        return -1
    return hour_counts.most_common(1)[0][0]


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    count = 0
    for entry in read_logs():
        if (entry.get('level') == 'CRITICAL' and
                '05:00:00' <= entry.get('time', '') <= '05:20:00'):
            count += 1
    return count


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    count = 0
    for entry in read_logs():
        if 'dog' in entry.get('message', '').lower():
            count += 1
    return count


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово (строка)
    """
    word_counts = Counter()
    for entry in read_logs():
        if entry.get('level') == 'WARNING':
            message = entry.get('message', '').lower()
            words = re.findall(r'\w+', message)
            word_counts.update(words)

    if not word_counts:
        return ""
    return word_counts.most_common(1)[0][0]


if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')