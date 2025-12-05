import logging
import random
import threading
import time

TOTAL_TICKETS = 100     
AVAILABLE_TICKETS = 10    

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.lock = semaphore
        logger.info('Director started work')

    def run(self):
        global TOTAL_TICKETS, AVAILABLE_TICKETS
        while TOTAL_TICKETS > 0:
            if AVAILABLE_TICKETS < 4:
                with self.lock:
                    tickets_to_print = min(10 - AVAILABLE_TICKETS, TOTAL_TICKETS)
                    AVAILABLE_TICKETS += tickets_to_print
                    TOTAL_TICKETS -= tickets_to_print
                    logger.info(f'Director put {tickets_to_print} new tickets (available={AVAILABLE_TICKETS}, total={TOTAL_TICKETS})')
        logger.info('Director stops work, no more tickets left.')

class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        self.tickets_sold = 0
        logger.info(f'Seller {self.name} started work')

    def run(self):
        global AVAILABLE_TICKETS
        while True:
            self.random_sleep()
            with self.sem:
                if AVAILABLE_TICKETS <= 0 and TOTAL_TICKETS <= 0:
                    break
                if AVAILABLE_TICKETS > 0:
                    self.tickets_sold += 1
                    AVAILABLE_TICKETS -= 1
                    logger.info(f'{self.name} sold one; available={AVAILABLE_TICKETS}, total={TOTAL_TICKETS}')
        logger.info(f'Seller {self.name} finished, sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.uniform(0, 0.5))

def main():
    semaphore = threading.Semaphore()
    director = Director(semaphore)
    director.start()

    sellers = []
    for _ in range(4):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()
    director.join()

if __name__ == '__main__':
    main()
