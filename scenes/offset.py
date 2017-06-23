import pygame
from pygame.locals import *

from scene import Scene
from scenes import Prompt, Success, EyesCalibration
from screen import boundary
from render import render
from .text import text


class Offset(Scene):
    def __init__(self, surface, fontname, parent=None, screen=None):
        super(Offset, self).__init__(surface, fontname, parent)
        self.screen = screen
        self.sub_surf = surface.subsurface(pygame.Rect((480, 540), (960, 540)))
        self.sub_window = EyesCalibration(self.sub_surf, fontname, self, screen, (480, 540))

    def process_event(self, event):
        if event.type == KEYUP and event.key in self.keys:
            self.process_key_event(event)
        else:
            self.sub_window.process_event(event)

    def draw(self):
        font = pygame.font.Font(self.fontname, 72)
        self.surface.fill(0)
        render(font, text['offset0'], surface=self.surface, topleft=(0, 0))
        render(font, text['offset1'], surface=self.surface, topleft=(0, 72))
        render(font, text['offset2'], surface=self.surface, topleft=(0, 144))
        render(font, text['offset9'], surface=self.surface, topleft=(0, 216))
        for x in boundary(self.screen.ppl, 1120, 800):
            for i in range(self.screen.wpl):
                pygame.draw.line(self.surface, (0, 255, 0), (x + i, 100), (x + i, 980))
            # for i in range(self.screen.offset + self.screen.wpl, self.screen.offset + self.screen.wpl * 2):
            #     pygame.draw.line(self.surface, (0, 0, 255), (x + i, 100), (x + i, 980))
        self.sub_window.draw()

    def esc(self, _):
        self.next_scene = Prompt(self.surface, self.fontname, self)

    def space(self, _):
        self.next_scene = Success(self.surface, self.fontname, self, self.screen)

    def z(self, _):
        self.next_scene = self.parent

    keys = {K_ESCAPE: esc, K_SPACE: space, K_z: z}
