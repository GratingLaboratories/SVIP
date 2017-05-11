import pygame
from pygame.locals import *


class Scene:
    keys = {}

    def __init__(self, surface, fontname, parent=None):
        self.surface = surface
        self.fontname = fontname
        self.parent = parent
        self.next_scene = self

    def process_event(self, event):
        if event.type == KEYUP:
            self.process_key_event(event)

    def process_key_event(self, event):
        self.keys.get(event.key, lambda s, e: None)(self, event)

    def draw(self):
        pass

    def tick(self):
        for event in pygame.event.get():
            self.process_event(event)
        self.draw()
        next_scene = self.next_scene
        self.next_scene = self
        return next_scene
