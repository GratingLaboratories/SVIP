from screen import boundary


def transform(surface, screen):
    result = surface.copy()
    if not hasattr(screen, 'ppl'):
        return result
    for x in boundary(screen.ppl, surface.get_width()):
        for y in range(surface.get_height()):
            colors = [surface.get_at((x + i, y)) for i in range(int(screen.ppl))]
            average = tuple(map(lambda l: sum(l) // len(l), zip(*colors)))
            for i in range(int(screen.ppl)):
                result.set_at((x + i, y), average)
    return result
