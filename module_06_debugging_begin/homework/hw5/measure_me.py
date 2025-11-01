import logging
import time
import random
from typing import List

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def measure_me(nums: List[int]) -> List[List[int]]:
    start = time.perf_counter()
    logger.debug("Enter measure_me")

    results = []
    nums.sort()

    for i in range(len(nums) - 2):
        left = i + 1
        right = len(nums) - 1
        target = 0 - nums[i]
        if i == 0 or nums[i] != nums[i - 1]:
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    results.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    left += 1
                else:
                    right -= 1

    elapsed = time.perf_counter() - start
    logger.debug(f"Leave measure_me, took {elapsed:.6f} seconds")
    return results

if __name__ == "__main__":
    durations = []
    for it in range(15):
        data_line = [random.randint(-(2**31), 2**31 - 1) for _ in range(10**3)]
        start = time.perf_counter()
        measure_me(data_line)
        durations.append(time.perf_counter() - start)

    avg = sum(durations) / len(durations)
    print(f"Среднее время выполнения measure_me: {avg:.6f} сек")