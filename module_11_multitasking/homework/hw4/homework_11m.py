import logging
import random
import threading
import time
from queue import PriorityQueue
from typing import Callable, Any

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


class Task:
    """Модель задачи с приоритетом, функцией и аргументами."""
    def __init__(self, priority: int, func: Callable, *args: Any) -> None:
        self.priority = priority
        self.func = func
        self.args = args

    def __lt__(self, other: "Task") -> bool:
        return self.priority < other.priority

    def run(self) -> None:
        logger.info(f">running Task(priority={self.priority}).\t {self.func.__name__}{self.args}")
        self.func(*self.args)


class Producer(threading.Thread):
    def __init__(self, queue: PriorityQueue) -> None:
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        logger.info("Producer: Running")
        for i in range(10):
            priority = random.randint(0, 6)
            delay = random.random()
            task = Task(priority, time.sleep, delay)
            self.queue.put(task)
        logger.info("Producer: Done")


class Consumer(threading.Thread):
    def __init__(self, queue: PriorityQueue) -> None:
        super().__init__()
        self.queue = queue

    def run(self) -> None:
        logger.info("Consumer: Running")
        while True:
            try:
                task: Task = self.queue.get(timeout=1)
            except Exception:
                break
            if task is None:
                break
            task.run()
            self.queue.task_done()
        logger.info("Consumer: Done")


def main() -> None:
    queue = PriorityQueue()

    producer = Producer(queue)
    consumer = Consumer(queue)

    producer.start()
    producer.join()

    consumer.start()
    consumer.join()


if __name__ == "__main__":
    main()
