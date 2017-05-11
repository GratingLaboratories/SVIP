import pygame
from pygame.locals import *

from scene import Scene
from scenes import Prompt
from render import render
from .text import text


class Success(Scene):
    def draw(self):
        font = pygame.font.Font(self.fontname, 48)
        self.surface.fill(0)
        render(font, text['success0'], surface=self.surface, topleft=(0, 0))
        # TODO
        render(font, text['success9'], surface=self.surface, bottomleft=(0, 1080))

    def esc(self, _):
        self.next_scene = Prompt(self.surface, self.fontname, self)

    def space(self, _):
        # TODO
        exit()

    keys = {K_ESCAPE: esc, K_SPACE: space}
