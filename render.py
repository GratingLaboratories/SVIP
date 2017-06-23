from time import time

n = 0
d = 1


def tick():
    global n, d
    n += d
    if d > 0 and n > 50 or d < 0 and n < 0:
        d = -d


def render(font, s, color=(255, 255, 255), surface=None, **kwargs):
    global n, d
    text = font.render(s, True, color)
    rect = text.get_rect()
    for k in kwargs:
        setattr(rect, k, kwargs[k])
    rect.left += n
    if surface is None:
        return text, rect
    else:
        surface.blit(text, rect)
