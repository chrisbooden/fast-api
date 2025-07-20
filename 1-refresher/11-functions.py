"""
Functions
"""

def add(x: int, y: int) -> int:
    """
    A function that returns the sum of two inputs
    """
    return x + y


print(f"The sum of 10 and 20 is {add(20,10)}")

# Anonymous functions
fun = lambda x, y : x + y 
print(f"The sum of 10 and 20 is {fun(20,10)}")

# Generator functions
def squares(x: list) -> iter:
    for y in x:
        yield y**2

x = [1, 2, 3, 4, 5]

sq = squares(x)
print(list(sq))
# for s in sq:
#     print(s)


# Use other decorators to enhance performance of functions if repeatedly called
from functools import lru_cache

@lru_cache(maxsize=1000)
def fib(i):
    if (i <= 2): return i

    return fib(i-1) + fib(i-2)

for i in range(1, 50):
    print(f"fib({i}) = {fib(i)}")
    
