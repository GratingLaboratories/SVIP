import pygame
from pygame.locals import *

from scene import Scene
from scenes import Prompt, Success
from screen import boundary
from render import render
from .text import text


class Wpl(Scene):
    def __init__(self, surface, fontname, parent=None, screen=None):
        super(Wpl, self).__init__(surface, fontname, parent)
        self.screen = screen
        self.screen.wpl = 1

    def draw(self):
        font = pygame.font.Font(self.fontname, 48)
        self.surface.fill((255, 255, 255))
        render(font, text['wpl0'], color=(0, 0, 0), surface=self.surface, topleft=(0, 0))
        render(font, text['wpl9'], color=(0, 0, 0), surface=self.surface, bottomleft=(0, 1080))
        for x in boundary(self.screen.ppl, self.surface.get_width()):
            for i in range(self.screen.wpl):
                pygame.draw.line(self.surface, (0, 0, 0), (int(x + i), 100), (int(x + i), 980))

    def esc(self, _):
        self.next_scene = Prompt(self.surface, self.fontname, self)

    def space(self, _):
        self.next_scene = Success(self.surface, self.fontname)

    def left(self, _):
        if self.screen.wpl > 1:
            self.screen.wpl -= 1

    def right(self, _):
        if self.screen.wpl < self.screen.ppl // 2:
            self.screen.wpl += 1

    def z(self, _):
        self.next_scene = self.parent

    keys = {K_ESCAPE: esc, K_SPACE: space, K_LEFT: left, K_RIGHT: right, K_z: z}
