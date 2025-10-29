import subprocess
import os
import signal
from typing import List
from flask import Flask

app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, занимающих переданный порт
    @param port: порт
    @return: список PID процессов, занимающих порт
    """
    if not isinstance(port, int):
        raise ValueError("Порт должен быть числом")

    try:
        result = subprocess.check_output(
            ["lsof", "-t", f"-i:{port}"], text=True
        )
        pids = [int(pid) for pid in result.strip().split("\n") if pid]
        return pids
    except subprocess.CalledProcessError:
        return []


def free_port(port: int) -> None:
    """
    Завершает процессы, занимающие переданный порт
    @param port: порт
    """
    pids: List[int] = get_pids(port)
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
            print(f"Процесс {pid} завершён (порт {port})")
        except ProcessLookupError:
            print(f"Процесс {pid} уже не существует")
        except PermissionError:
            print(f"Нет прав для завершения процесса {pid}")


def run(port: int) -> None:
    """
    Запускает flask-приложение по переданному порту.
    Если порт занят каким-либо процессом, завершает его.
    @param port: порт
    """
    free_port(port)
    app.run(port=port)


if __name__ == '__main__':
    run(5000)