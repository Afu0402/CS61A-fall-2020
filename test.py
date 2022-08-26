class Link:
    empty = ()

    def __init__(self, first, rest=empty):
        assert isinstance(rest, Link) or rest is Link.empty, "rest must be a Link"
        self.first = first
        self.rest = rest

    def __str__(self):
        print("1212")
        if self is Link.empty:
            return "empty"
        return str(self.first) + "," + str(self.rest)

    __repr__ = __str__


odd = lambda x: x % 2 == 1

"""
link  3  4  5  + 0
 0  3  4  5  + 9
 0 3  4  5  9 + 7
 0 3  4 5 7 9 

"""


def add(s, v):
    if v < s.first:
        s.first, s.rest = v, Link(s.first, s.rest)
    elif v > s.first and s.rest is not Link.empty:
        add(s.rest, v)
    elif v > s.first:
        s.rest = Link(v)
    return s


def filter_link(fn, s):
    if s is Link.empty:
        return s
    print(s.first)
    filter_rest = filter_link(fn, s.rest)
    if fn(s.first):
        return Link(s.first, filter_rest)
    else:
        return filter_rest


class Tree:
    def __init__(self, label, branches=[]):
        self.label = label
        self.branches = list(branches)

    def __repr__(self):
        if self.branches:
            str = ", " + repr(self.branches)
        else:
            str = ""
        return "Tree({0}{1})".format(repr(self.label), str)

    def __str__(self):
        return "\n".join(self.indented())

    def indented(self):
        lines = []
        for b in self.branches:
            for line in b.indented():
                lines.append("  " + line)
        return [str(self.label)] + lines


s = Tree(3, [Tree(5), Tree(6)])
# print(filter_link(odd, s))
