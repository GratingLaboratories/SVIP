import pygame
import cv2

from pygame.locals import *
from pygame import surfarray
from universal import *
from scene import Scene
from cv.tracker import Tracker, Eye


class CameraError(Exception):
    pass


class EyesCalibration(Scene):
    def __init__(self, surface, fontname, parent, screen, offset):
        """
        :param surface: 
        :param fontname: 
        :param parent: 
        :param screen: 
        :param offset: (left, top) 
        """
        Scene.__init__(self, surface, fontname, parent)
        self.screen = screen
        self.screen.positions = []
        self.cap = cv2.VideoCapture(0)
        ret, frame = self.cap.read()
        try:
            height, width, channel = frame.shape
        except ValueError:
            logging.warning("Camera may work in B/W mode")
            try:
                height, width = frame.shape
            except ValueError:
                logging.critical("Fail to load camera module.")
                raise CameraError

        if height * width < 153600:
            logging.warning("Your camera's resolution is too low, " +
                            "please consider switching to a higher resolution camera for better performance.")

        surf_width, surf_height = surface.get_size()
        width_ratio = surf_width / width
        height_ratio = surf_height / height
        self.ratio = min(width_ratio, height_ratio)
        self.tracker = Tracker(Eye(20), width, height)
        self.position = (0, 0)
        self.offset = offset
        self.colors = [(0xFF, 0, 0), (0xFF, 0xD7, 0), (0, 0xFF, 0xFF), (0, 0x66, 0x66), (0, 0, 0xFA),
                       (0xE3, 0x23, 0x26), (0, 0xFF, 0x80), (0xFF, 0x24, 0), (0xFF, 0xFF, 00)]

    def process_event(self, event):
        if event.type == KEYUP:
            func = EyesCalibration.keys.get(event.key, None)
            if func:
                func()

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            off_x, off_y = self.offset
            click = (x - off_x, y - off_y)
            click[0] /= self.ratio
            click[1] /= self.ratio
            self.tracker.change_pos(click[0], click[1])

    def draw(self):
        frame = self.capture()
        c_index = 0
        for pos in self.screen.positions:
            x, y = pos
            start = (x - 3, y - 3)
            end = (x + 3, y + 3)
            cv2.rectangle(frame, start, end, self.colors[c_index], 2)
            c_index += 1
            c_index %= len(self.colors)

        frame = cv2.resize(frame, None, fx=self.ratio, fy=self.ratio, interpolation=cv2.INTER_CUBIC)
        camera = surfarray.make_surface(frame)
        self.surface.blit(camera, (0, 0))

    def capture(self):
        rect, frame = self.cap.read()
        self.position = self.tracker.update(frame)
        return frame

    def tick(self):
        for event in pygame.event.get():
            self.process_event(event)
        self.draw()
        next_scene = self.next_scene
        self.next_scene = self
        return next_scene

    def add_new_pos(self):
        self.screen.positions.append(self.position)

    def delete_pos(self):
        self.screen.positions.pop(-1)

    keys = {K_SPACE: add_new_pos, K_DELETE: delete_pos}
