"""
Questions
1.1 Write a function that takes in a number n and returns a one-argument function.
The returned function takes in a function that is used to update n. It should return
the updated n.
"""


def memory(n):
    """
    >>> f = memory(10)
    >>> f(lambda x: x * 2)
    20
    >>> f(lambda x: x - 7)
    13
    >>> f(lambda x: x > 5)
    True"""

    def f(fn):
        nonlocal n
        n = fn(n)
        return n

    return f


def add_this_many(x, el, s):
    """Adds el to the end of s the number of times x occurs
    in s.
    >>> s = [1, 2, 4, 2, 1]
    >>> add_this_many(1, 5, s)
    >>> s
    [1, 2, 4, 2, 1, 5, 5]
    >>> add_this_many(2, 2, s)
    >>> s
    [1, 2, 4, 2, 1, 5, 5, 2, 2]"""
    add_arr = [el for same_elem in s if same_elem == x]
    s.extend(add_arr)


def filter(iterable, fn):
    """
    >>> is_even = lambda x: x % 2 == 0
    >>> list(filter(range(5), is_even)) # a list of the values yielded from the call to filter
    [0, 2, 4]
    >>> all_odd = (2*y-1 for y in range(5))
    >>> list(filter(all_odd, is_even))
    []
    >>> naturals = (n for n in range(1, 100))
    >>> s = filter(naturals, is_even)
    >>> next(s)
    2
    >>> next(s)
    4"""
    for x in iterable:
        if fn(x):
            yield x


is_even = lambda x: x % 2 == 0

# print(list(filter(range(5), is_even)))
# all_odd = (2 * y - 1 for y in range(5))
# print(list(filter(all_odd, is_even)))


def merge(a, b):
    """
    >>> def sequence(start, step):
    ... while True:
    ... yield start
    ... start += step
    >>> a = sequence(2, 3) # 2, 5, 8, 11, 14, ...
    >>> b = sequence(3, 2) # 3, 5, 7, 9, 11, 13, 15, ...
    >>> result = merge(a, b) # 2, 3, 5, 7, 8, 9, 11, 13, 14, 15
    >>> [next(result) for _ in range(10)]
    [2, 3, 5, 7, 8, 9, 11, 13, 14, 15]"""
    res = []
    while True:
        a_value = next(a)
        yield a_value
        b_value = next(b)
        if b_value == a_value:
            b_value = next(b)
        yield b_value


def sequence(start, step):
    while True:
        yield start
        start += step


a = sequence(2, 3)  # 2, 5, 8, 11, 14, ...
b = sequence(3, 2)  # 3, 5, 7, 9,
result = merge(a, b)
# print(next(result))
# print(next(result))
# print(next(result))
print([next(result) for _ in range(20)])
