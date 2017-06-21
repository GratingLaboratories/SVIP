import pygame
from pygame.locals import *

from scene import Scene
from scenes import EyesCalibration
from screen import boundary, Screen
from render import render
from .text import text


class Offset(Scene):
    def __init__(self, surface, fontname, parent=None, screen=None):
        super(Offset, self).__init__(surface, fontname, parent)
        self.screen = screen
        s = Screen()
        s.ppl = screen['ppl']
        s.wpl = screen['wpl']
        self.sub_surf = surface.subsurface(pygame.Rect((480, 540), (960, 540)))
        self.sub_window = EyesCalibration(self.sub_surf, fontname, self, s, (480, 540))

    def process_event(self, event):
        if event.type == KEYUP and event.key in self.keys:
            self.process_key_event(event)
        else:
            self.sub_window.process_event(event)

    def draw(self):
        self.surface.fill(0)
        begin = int((self.sub_window.position[0] - self.screen['offset'])
                / self.screen['period'] % 1. * self.screen['ppl'])
        for x in boundary(self.screen['ppl'], 1120, 800):
            for i in range(begin, begin + self.screen['wpl']):
                pygame.draw.line(self.surface, (0, 255, 0), (x + i, 100), (x + i, 980))
            # for i in range(self.screen.offset + self.screen.wpl, self.screen.offset + self.screen.wpl * 2):
            #     pygame.draw.line(self.surface, (0, 0, 255), (x + i, 100), (x + i, 980))
        self.sub_window.draw()

    def esc(self, _):
        exit()

    keys = {K_ESCAPE: esc, K_SPACE: esc}
