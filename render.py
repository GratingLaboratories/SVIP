def render(font, s, color=(255, 255, 255), surface=None, **kwargs):
    text = font.render(s, True, color)
    rect = text.get_rect()
    for k in kwargs:
        setattr(rect, k, kwargs[k])
    if surface is None:
        return text, rect
    else:
        surface.blit(text, rect)
