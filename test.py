def min_abs_indices(s):
    """
    >>> min_abs_indices([-4,-3,-2,3,2,4])
    [2,4]
    """
    min_num = min(list(map(lambda x: abs(x), s)))

    return [i for i in range(len(s)) if abs(s[i]) == min_num]


print(min_abs_indices([-4, -3, -2, 3, 2, 4]))


def largest_adj_sum(s):

    if len(s) == 1:
        return s[0]
    return max([s[0] + s[1], largest_adj_sum(s[1:])])


print(largest_adj_sum([-4, -3, -2, 3, 2, 4]))


def digit_dict(s):
    dic = {}
    for item in s:
        if item < 10:
            key = item
        else:
            key = item % 10
        value = [x for x in s if x == key or x % 10 == key]
        dic[key] = value
    return dic


print(digit_dict([5, 8, 13, 21, 34, 55, 89]))


def all_have_an_equal(s):
    for i in range(len(s)):
        if s[i] not in s[:i] + s[i + 1 :]:
            return False
    return True


print(all_have_an_equal([-4, -3, 4, 3]))
print(all_have_an_equal([4, 3, 2, 3, 2, 4]))
