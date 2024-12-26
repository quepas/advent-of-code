from functools import reduce


def apply(x, f):
    return f(x)


def compose(*callables):
    """
    Compose functions from left-to-right
        f1, f2, f3 ... -> f3(f2(f1(...)))
    Just like function application $ from Haskell ;) Well, we need to compose-apply in Python
    """
    return lambda x: reduce(apply, callables, x)
