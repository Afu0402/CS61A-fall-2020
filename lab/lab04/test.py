def rational(n, d):
    def selector(y):
        if y == "n":
            return n
        elif y == "d":
            return d

    return selector


def numer(x):
    return x("n")


def denom(x):
    return x("d")
