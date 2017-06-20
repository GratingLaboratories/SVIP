import pygame
from pygame.locals import *

from scene import Scene
from render import render
from .text import text


class Prompt(Scene):
    def draw(self):
        font = pygame.font.Font(self.fontname, 128)
        pygame.draw.rect(self.surface, (0, 0, 0), Rect((100, 100), (1720, 880)))
        pygame.draw.lines(self.surface, (255, 255, 255), True,
                          [(100, 100), (1820, 100), (1820, 980), (100, 980)], 5)
        render(font, text['prompt0'], surface=self.surface, topleft=(100, 100))
        render(font, text['prompt9'], surface=self.surface, bottomleft=(100, 980))

    def esc(self, _):
        self.next_scene = self.parent

    @staticmethod
    def space(_):
        exit()

    keys = {K_ESCAPE: esc, K_SPACE: space}
