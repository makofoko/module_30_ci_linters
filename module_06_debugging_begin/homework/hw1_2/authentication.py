import getpass
import hashlib
import logging
import sys

WEAK_WORDS_LIST = [
    "password", "admin", "root", "test", "login", "user", 
    "skillbox", "admin123", "qwerty"
]

logger = logging.getLogger("password_checker")


def is_strong_password(password: str) -> bool:
    """
    ЗАДАЧА 2: Проверяет, что пароль НЕ содержит 
    английских слов из списка WEAK_WORDS_LIST.
    """
    password_lower = password.lower()
    
    for word in WEAK_WORDS_LIST:
        if word in password_lower:
            logger.warning(f"Пароль содержит недопустимое слово: '{word}'")

            return False
    return True


def input_and_check_password() -> bool:
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()

    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False

    if not is_strong_password(password):
        return False

    try:
        hasher = hashlib.md5()
        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            logger.info("Пароль верный.")
            return True
        else:
            logger.warning("Введен неверный пароль.")
            
    except ValueError as ex:
        logger.exception("Вы ввели некорректный символ, который не кодируется в latin-1.")

    return False


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        filename='stderr.txt',
        filemode='w',
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    logger.info("Логгер успешно сконфигурирован.")

    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")
    count_number: int = 3
    logger.info(f"У вас есть {count_number} попыток")

    while count_number > 0:
        if input_and_check_password():
            logger.info("Успешная аутентификация.")
            exit(0)
            
        count_number -= 1
        if count_number > 0:
            logger.warning(f"Неверно. Осталось попыток: {count_number}")

    logger.error("Пользователь трижды ввёл не правильный пароль! Блокировка.")
    exit(1)