import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10          
MAX_SEATS: int = 30       
SELLERS_COUNT: int = 3          
THRESHOLD: int = 4          
ADD_COUNT: int = 6              

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.tickets_sold: int = 0
        logger.info(f'Продавец {self.name} создан')

    def run(self) -> None:
        global TOTAL_TICKETS
        logger.info(f'Продавец {self.name} начал работу')
        while True:
            time.sleep(random.uniform(0.2, 0.5))  # имитация времени обслуживания
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} продал билет; осталось {TOTAL_TICKETS}')
        logger.info(f'Продавец {self.name} завершил работу, продал {self.tickets_sold} билетов')


class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.replenishments: int = 0
        logger.info('Директор создан')

    def run(self) -> None:
        global TOTAL_TICKETS
        logger.info('Директор начал работу')
        while True:
            time.sleep(0.1) 
            with self.sem:
                if TOTAL_TICKETS >= MAX_SEATS or TOTAL_TICKETS <= 0:
                    break
                if TOTAL_TICKETS <= THRESHOLD:
                    to_add = min(ADD_COUNT, MAX_SEATS - TOTAL_TICKETS)
                    if to_add > 0:
                        logger.info(f'Директор печатает {to_add} билетов (было {TOTAL_TICKETS})')
                        time.sleep(1.0)  
                        TOTAL_TICKETS += to_add
                        self.replenishments += 1
                        logger.info(f'Директор закончил печать: теперь {TOTAL_TICKETS} билетов')
        logger.info(f'Директор завершил работу, пополнил {self.replenishments} раз')


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore()
    sellers: List[Seller] = [Seller(semaphore) for _ in range(SELLERS_COUNT)]
    director: Director = Director(semaphore)

    for s in sellers:
        s.start()
    director.start()

    for s in sellers:
        s.join()
    director.join()

    total_sold = sum(s.tickets_sold for s in sellers)
    logger.info(f'Всего продано: {total_sold}. Осталось билетов: {TOTAL_TICKETS}')


if __name__ == '__main__':
    main()
