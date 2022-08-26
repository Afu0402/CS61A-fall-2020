def count_k(n, k):
    """counts the number of paths up a flight of stairs
    when taking up to and including k steps at a time
    >>> count_k(3,3) # 3, 2+1, 1+2, 1+1+1
    4
    >>> count_k(4,4)
    8
    """
    if n == 0:
        return 1
    if n < 0:
        return 0
    total = 0
    i = 1
    while i <= k:
        total += count_k(n - i, k)
        i += 1
    return total


def max_product(s):
    """Return the maximum product that can be formed using non-consecutive elements of s
    >>> max_product([10,3,1,9,2]) # 10 * 9
    90
    >>> max_product([5,10,5,10,5]) # 5 * 5 * 5
    125
    >>> max_product([])
    1
    """
    if s == []:
        return 1
    else:
        return max(max_product(s[1:]), s[0] * max_product(s[2:]))
