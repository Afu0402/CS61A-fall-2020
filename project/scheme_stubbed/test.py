from multiprocessing.sharedctypes import Value
from this import d
from black import InvalidInput

_WHITESPACE = set(" \t\n\r")


class InputReader:
    def __init__(self, prompt):
        self.prompt = prompt

    def __iter__(self):
        while True:
            res = input(self.prompt)
            yield res
            self.prompt = " " * len(self.prompt)


class Buffer:
    def __init__(self, source):
        self.index = 0
        self.current_line = ()
        self.source = source
        self.current()

    def pop_first(self):
        current = self.current()
        self.index += 1
        return current

    def current(self):
        while not self.more_on_line:
            try:
                self.index = 0
                self.current_line = next(self.source)
            except StopIteration:
                self.current_line = ()
                return None
        return self.current_line[self.index]

    @property
    def more_on_line(self):
        return self.index < len(self.current_line)


def read(line, k):
    result = []
    while k < len(line):
        c = line[k]
        if c in _WHITESPACE:
            k += 1
        else:
            result.append(line[k])
            k += 1
    return result


def token_line():

    return (read(line, 0) for line in InputReader("afu> "))


class Nil:
    def __repr__(self):
        return "nil"

    def __str__(self):
        return "nil"

    def __len__():
        return 0


nil = Nil()


def read_tail(src):
    if not src.current():
        raise SyntaxError("unknown token", src.current())
    if src.current() == ")":
        src.pop_first()
        return nil
    return Pair(scheme_read(src), read_tail(src))


def scheme_read(src):
    val = src.pop_first()
    if val == "(":
        return read_tail(src)
    try:
        val = int(val)
        return val
    except ValueError:
        return val


class Pair(object):
    def __init__(self, first, rest=nil):
        if not isinstance(rest, Pair) and rest is not nil:

            print(rest)
            raise ValueError("rest must be an instance of Piar or nil")
        self.first = first
        self.rest = rest

    def __repr__(self):
        # if self.rest is nil:
        #     return repr(nil)
        return "Pair(" + repr(self.first) + "," + repr(self.rest) + ")"

    def map(self, fn):
        first_res = fn(self.first)
        if self.rest is nil:
            return Pair(first_res, nil)
        return Pair(first_res, self.rest.map(fn))


def suqare(x):
    print("x", x)
    if isinstance(x, int):
        return x * 2
    return x


while True:
    try:
        src = Buffer(token_line())
        expr = ""
        while src.more_on_line:
            expr = scheme_read(src)
        print("str", expr)
        print("expr", repr(expr))
        if isinstance(expr, Pair):
            print(expr.map(suqare))
    except EOFError:
        raise SyntaxError("unexpected end of file")
