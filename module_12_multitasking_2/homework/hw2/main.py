import subprocess

def process_count(username: str) -> int:
    """
    Количество процессов, запущенных от имени пользователя username.
    """
    try:
        result = subprocess.run(
            ["ps", "-u", username, "-o", "pid="],
            capture_output=True, text=True, check=True
        )
        return len(result.stdout.strip().splitlines())
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при вызове ps: {e}")
        return 0


def _collect_descendants(pid: str) -> list[str]:
    """Рекурсивно собираем всех потомков процесса."""
    result = subprocess.run(
        ["pgrep", "-P", pid],
        capture_output=True, text=True
    )
    children = result.stdout.strip().splitlines() if result.stdout else []
    all_pids = children[:]
    for child in children:
        all_pids.extend(_collect_descendants(child))
    return all_pids


def total_memory_usage(root_pid: int) -> float:
    """
    Суммарное потребление памяти (в %) для процесса root_pid и всех его потомков.
    """
    try:
        all_pids = [str(root_pid)] + _collect_descendants(str(root_pid))

        total_mem = 0.0
        for pid in all_pids:
            ps_result = subprocess.run(
                ["ps", "-p", pid, "-o", "pmem="],
                capture_output=True, text=True
            )
            if ps_result.stdout.strip():
                total_mem += float(ps_result.stdout.strip())
        return total_mem
    except Exception as e:
        print(f"Ошибка при вычислении памяти: {e}")
        return 0.0