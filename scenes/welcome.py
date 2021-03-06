import pygame
from pygame.locals import *

from scene import Scene
from scenes import Ppl
from render import render
from screen import Screen
from .text import text


class Welcome(Scene):
    def draw(self):
        font = pygame.font.Font(self.fontname, 72)
        self.surface.fill(0)
        render(font, text['welcome0'], surface=self.surface, topleft=(0, 0))
        render(font, text['welcome9'], surface=self.surface, topleft=(0, 72))

    def esc(self, _):
        exit()

    def space(self, _):
        self.next_scene = Ppl(self.surface, self.fontname, self, Screen())

    keys = {K_ESCAPE: esc, K_SPACE: space}
