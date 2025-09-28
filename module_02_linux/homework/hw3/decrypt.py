import sys


def decrypt(cipher: str) -> str:
    """
    Расшифровывает строку по правилам:
    - буквы и пробелы добавляются как есть;
    - '.' после символа означает: оставить символ, точку удалить;
    - '..' означает: удалить предыдущий символ и сами точки.
    """
    result = []
    i = 0
    while i < len(cipher):
        ch = cipher[i]

        if ch == "." and i + 1 < len(cipher) and cipher[i + 1] == ".":
            if result:
                result.pop()  
            i += 2  
            continue

        if ch == ".":
            i += 1  
            continue

        result.append(ch)
        i += 1

    return "".join(result)


def main() -> None:
    """
    Читает входные данные из stdin и выводит результат.
    """
    data = sys.stdin.read().strip()
    if not data:
        print("")  
        return

    print(decrypt(data))


if __name__ == "__main__":
    main()
