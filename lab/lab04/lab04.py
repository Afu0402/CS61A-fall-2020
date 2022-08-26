HW_SOURCE_FILE = __file__


def line_stepper(start, k):
    """
    Complete the function line_stepper, which returns the number of ways there are to go from start to 0 on the number line by taking exactly k steps along the number line.
    """ """
    Complete the function line_stepper, which returns the number of ways there are to go from
    start to 0 on the number line by taking exactly k steps along the number line.

    >>> line_stepper(1, 1)
    1
    >>> line_stepper(0, 2)
    2
    >>> line_stepper(-3, 3)
    1
    >>> line_stepper(3, 5)
    5
    """
    "*** YOUR CODE HERE ***"
    if k < 0:
        return 0
    if k == 0:
        return 1 if start == 0 else 0

    return line_stepper(start - 1, k - 1) + line_stepper(start + 1, k - 1)


def summation(n, term):
    """Return the sum of numbers 1 through n (including n) wíth term applied to each number.
    Implement using recursion!

    >>> summation(5, lambda x: x * x * x) # 1^3 + 2^3 + 3^3 + 4^3 + 5^3
    225
    >>> summation(9, lambda x: x + 1) # 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10
    54
    >>> summation(5, lambda x: 2**x) # 2^1 + 2^2 + 2^3 + 2^4 + 2^5
    62
    >>> # Do not use while/for loops!
    >>> from construct_check import check
    >>> # ban iteration
    >>> check(HW_SOURCE_FILE, 'summation',
    ...       ['While', 'For'])
    True
    """
    assert n >= 1
    "*** YOUR CODE HERE ***"
    if n == 1:
        return term(1)
    return term(n) + summation(n - 1, term)


def paths(m, n):
    """Return the number of paths from one corner of an
    M by N grid to the opposite corner.

    >>> paths(2, 2)
    2
    >>> paths(5, 7)
    210
    >>> paths(117, 1)
    1
    >>> paths(1, 157)
    1
    """
    "*** YOUR CODE HERE ***"
    if m == 1 or n == 1:
        return 1
    return paths(m - 1, n) + paths(m, n - 1)


def pascal(row, column):
    """Returns the value of the item in Pascal's Triangle
    whose position is specified by row and column.
    >>> pascal(0, 0)
    1
    >>> pascal(0, 5)	# Empty entry; outside of Pascal's Triangle
    0
    >>> pascal(3, 2)	# Row 3 (1 3 3 1), Column 2
    3
    >>> pascal(4, 2)     # Row 4 (1 4 6 4 1), Column 2
    6
    """
    "*** YOUR CODE HERE ***"

    def helper_make_row(n):
        if len(n) <= 1:
            return []

        return [n[0] + n[1]] + helper_make_row(n[1:])

    def make_row(n):
        if len(n) == 0:
            return [1]
        if len(n) == 1:
            return [1, 1]
        return [1] + helper_make_row(n) + [1]

    def helper(row, column, seq):
        if row < 0:
            return seq[column] if column < len(seq) else 0
        return helper(row - 1, column, make_row(seq))

    return helper(row, column, [])
