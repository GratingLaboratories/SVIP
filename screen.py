def boundary(ppl, end=None, begin=0):
    end -= ppl
    x = float(begin)
    while end is None or x < end:
        yield int(x)
        x += ppl


class Screen:
    pass
