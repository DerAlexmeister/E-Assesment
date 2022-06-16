import time

from random import seed
from random import randint

def generateNumbers(max, amount=4):
    numbers = []
    try:
        for _ in range(amount): 
            seed(time.time_ns())
            numbers.append(randint(0, max))
            time.sleep(0.5)
        return numbers
    except Exception as error:
        print(error)
        return None