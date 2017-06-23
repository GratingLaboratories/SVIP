import pygame
from pygame.locals import *

from scene import Scene
from scenes import Prompt, Verify
from render import render
from .text import text


class Success(Scene):
    def __init__(self, surface, fontname, parent=None, screen=None):
        super(Success, self).__init__(surface, fontname, parent)
        poss = screen.positions
        left = min(poss.keys())
        right = max(poss.keys())
        l_av = sum(map(lambda x: x[0], poss[left])) / len(poss[left])
        r_av = sum(map(lambda x: x[0], poss[right])) / len(poss[right])
        screen.period = (l_av - r_av) / (right - left)
        screen.offset = l_av
        self.screen = screen

    def draw(self):
        font = pygame.font.Font(self.fontname, 72)
        self.surface.fill(0)
        render(font, text['success0'], surface=self.surface, topleft=(0, 0))
        render(font, text['success1'] % (self.screen.ppl,
                                         self.screen.wpl,
                                         self.screen.period,
                                         self.screen.offset),
               surface=self.surface, topleft=(0, 72))
        render(font, text['success9'], surface=self.surface, bottomleft=(0, 1080))

    def esc(self, _):
        self.next_scene = Prompt(self.surface, self.fontname, self)

    def space(self, _):
        screen = dict(ppl=self.screen.ppl,
                      wpl=self.screen.wpl,
                      period=self.screen.period,
                      offset=self.screen.offset)
        with open('screen.conf', 'w') as f:
            f.write(repr(screen))
        self.next_scene = Verify(self.surface, self.fontname, self, screen)

    keys = {K_ESCAPE: esc, K_SPACE: space}
