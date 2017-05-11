import pygame
from pygame.locals import *

from scene import Scene
from scenes import Prompt, Wpl
from screen import boundary
from render import render
from .text import text


class Ppl(Scene):
    def __init__(self, surface, fontname, parent=None, screen=None):
        super(Ppl, self).__init__(surface, fontname, parent)
        self.screen = screen
        self.screen.ppl = 10.
        self.step = 0.1

    def draw(self):
        font = pygame.font.Font(self.fontname, 128)
        self.surface.fill(0)
        render(font, text['ppl0'], surface=self.surface, topleft=(0, 0))
        render(font, text['ppl1'], surface=self.surface, topleft=(0, 128))
        render(font, text['ppl2'] % self.step, surface=self.surface, topleft=(0, 256))
        render(font, text['ppl3'] % self.screen.ppl, surface=self.surface, topleft=(0, 384))
        render(font, text['ppl7'], surface=self.surface, bottomleft=(0, 1080-128*2))
        render(font, text['ppl8'], surface=self.surface, bottomleft=(0, 1080-128))
        render(font, text['ppl9'], surface=self.surface, bottomleft=(0, 1080))
        for x in boundary(self.screen.ppl, self.surface.get_width()):
            pygame.draw.line(self.surface, (0, 255, 0), (x, 100), (x, 980))

    def esc(self, _):
        self.next_scene = Prompt(self.surface, self.fontname, self)

    def space(self, _):
        self.next_scene = Wpl(self.surface, self.fontname, self, self.screen)

    def left(self, _):
        if self.screen.ppl > self.step + 1:
            self.screen.ppl -= self.step

    def right(self, _):
        self.screen.ppl += self.step

    def up(self, _):
        self.step *= 10

    def down(self, _):
        self.step /= 10

    keys = {K_ESCAPE: esc, K_SPACE: space, K_LEFT: left, K_RIGHT: right, K_UP: up, K_DOWN: down}
