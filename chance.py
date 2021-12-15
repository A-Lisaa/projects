from random import random
from timeit import timeit

def chance_func(_chance):
    return bool(random() < _chance)

chance_lambda = lambda _chance: bool(random() < _chance)

print(timeit("chance_func(0.33)", number = 10000, globals = globals()))
print(timeit("chance_lambda(0.33)", number = 10000, globals = globals()))
print(timeit("bool(random() < 0.33)", number = 10000, globals = globals()))
