def neighbor_digits2(num, prev_digit=-1):
    if num < 10:
        return num == prev_digit
    last = num % 10
    rest = num // 10
    return int(last == rest % 10 or prev_digit == last) + neighbor_digits2(
        rest, prev_digit=last
    )


def has_subseq(n, seq):
    """
    Complete has_subseq, a function which takes in a number n and a "sequence"
    of digits seq and returns whether n contains seq as a subsequence, which
    does not have to be consecutive.

    >>> has_subseq(123, 12)
    True
    >>> has_subseq(141, 11)
    True
    >>> has_subseq(144, 12)
    False
    >>> has_subseq(144, 1441)
    False
    >>> has_subseq(1343412, 134)
    True
    """
    "*** YOUR CODE HERE ***"
    if seq == 0:
        return True
    if n == 0 and seq:
        return False

    if n % 10 == seq % 10:
        return has_subseq(n // 10, seq // 10)
    else:
        return has_subseq(n // 10, seq)


print(has_subseq(141, 11))
