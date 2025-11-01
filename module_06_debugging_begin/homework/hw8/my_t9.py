import sys
from typing import List, Dict
from collections import defaultdict

T9_MAP = {
    '2': 'abc',
    '3': 'def',
    '4': 'ghi',
    '5': 'jkl',
    '6': 'mno',
    '7': 'pqrs',
    '8': 'tuv',
    '9': 'wxyz'
}

WORDS_FILE = "words_alpha.txt"

REVERSE_T9_MAP: Dict[str, str] = {}
for digit, letters in T9_MAP.items():
    for letter in letters:
        REVERSE_T9_MAP[letter] = digit

def load_word_list() -> Dict[str, List[str]]:
    """
    Читает файл WORDS_FILE и создает карту:
    { "цифровая_последовательность": ["список", "слов"] }
    """
    processed_map = defaultdict(list)

    try:
        with open(WORDS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().lower()

                if not word.isalpha():
                    continue

                t9_sequence = []
                for char in word:
                    digit = REVERSE_T9_MAP.get(char)
                    if digit:
                        t9_sequence.append(digit)
                    else:
                        t9_sequence = [] # Очищаем
                        break

                if t9_sequence:
                    key = "".join(t9_sequence)
                    processed_map[key].append(word)

    except FileNotFoundError:
        print(f"ОШИБКА: Файл словаря '{WORDS_FILE}' не найден!", file=sys.stderr)
        print("Пожалуйста, создайте этот файл.", file=sys.stderr)

    return processed_map

print(f"Загрузка словаря из {WORDS_FILE}...")
T9_WORD_MAP = load_word_list()
print(f"Словарь загружен. Найдено {len(T9_WORD_MAP)} уникальных T9-последовательностей.")



def my_t9(input_numbers: str) -> List[str]:
    """
    Находит все английские слова,
    соответствующие T9-последовательности,
    используя заранее обработанную карту T9_WORD_MAP.
    """
    return T9_WORD_MAP.get(input_numbers, [])


if __name__ == '__main__':
    print("\nВведите T9-последовательность (например, 22736368):")
    numbers: str = input()
    words: List[str] = my_t9(numbers)

    if words:
        print("\nНайденные слова:")
        print(*words, sep='\n')
    else:
        print(f"\nСлов для последовательности '{numbers}' не найдено.")
