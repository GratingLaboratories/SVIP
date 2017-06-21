import pygame
import cv2
import numpy as np

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
        self.screen.positions = {}
        self.cap = cv2.VideoCapture(0)
        ret, frame = self.cap.read()
        try:
            height, width, channel = frame.shape
        except ValueError:
            logging.warning("Camera may work in B/W mode")
            try:
                width, height = frame.shape
            except ValueError:
                logging.critical("Fail to load camera module.")
                raise CameraError

        if height * width < 153600:
            logging.warning("Your camera's resolution is too low, " +
                            "please consider switching to a higher resolution camera for better performance.")

        surf_width, surf_height = surface.get_size()
        self.dims = (width, height)
        width_ratio = surf_width / width
        height_ratio = surf_height / height
        self.ratio = min(width_ratio, height_ratio)
        self.tracker = Tracker(Eye(30), width, height)
        self.position = (0, 0)
        self.offset = offset
        self.colors = [(0xFF, 0, 0), (0xFF, 0xD7, 0), (0, 0xFF, 0xFF), (0, 0x66, 0x66), (0, 0, 0xFA),
                       (0xE3, 0x23, 0x26), (0, 0xFF, 0x80), (0xFF, 0x24, 0), (0xFF, 0xFF, 00)]

    def process_event(self, event):
        if event.type == KEYUP:
            func = EyesCalibration.keys.get(event.key, None)
            if func:
                func(self, event)

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            off_x, off_y = self.offset
            click = [x - off_x, y - off_y]
            click[0] /= self.ratio
            click[1] /= self.ratio
            # print(click)
            self.tracker.change_pos(self.dims[0] - click[0], click[1])

    def draw(self):
        frame = self.capture()
        c_index = 0
        for group in self.screen.positions:
            for pos in self.screen.positions[group]:
                x, y = pos
                x = int(x + 0.5)
                y = int(y + 0.5)
                start = (x - 3, y - 3)
                end = (x + 3, y + 3)
                cv2.rectangle(frame, start, end, self.colors[c_index], 2)
                c_index += 1
                c_index %= len(self.colors)

        x, y = self.position
        start = (int(x + 0.5) - 10, int(y + 0.5) - 10)
        end = (int(x + 0.5) + 10, int(y + 0.5) + 10)
        cv2.rectangle(frame, start, end, (0xFF, 0xFF, 0), 1)

        width, height, channel = frame.shape
        frame = np.swapaxes(frame, 0, 1)
        n_frame = frame.copy()
        n_frame[:, :, 0] = frame[:, :, 2]
        n_frame[:, :, 2] = frame[:, :, 0]

        frame = cv2.resize(n_frame, None, fx=self.ratio, fy=self.ratio, interpolation=cv2.INTER_CUBIC)
        frame = np.flip(frame, 0)
        camera = surfarray.make_surface(frame)
        self.surface.blit(camera, (0, 0))

    def capture(self):
        rect, frame = self.cap.read()
        self.position = self.tracker.update(frame)
        # self.position = self.tracker.bact.x, self.tracker.bact.y
        # print('Position:', self.position)

        return frame

    def tick(self):
        for event in pygame.event.get():
            self.process_event(event)
        self.draw()
        next_scene = self.next_scene
        self.next_scene = self
        return next_scene

    def add_new_pos(self, event):
        self.screen.positions.setdefault(event.key, [])
        self.screen.positions[event.key].append(self.position)

    keys = {K_1: add_new_pos,
            K_2: add_new_pos,
            K_3: add_new_pos,
            K_4: add_new_pos,
            K_5: add_new_pos,
            K_6: add_new_pos,
            K_7: add_new_pos,
            K_8: add_new_pos,
            K_9: add_new_pos}
