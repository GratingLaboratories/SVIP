import cv2
import numpy as np


def bg_generator(time, dims, fps=20):
    frame_num = round(time * fps)
    for i in range(frame_num):
        green = np.zeros((dims[1], dims[0], 3), np.uint8)
        green[:, :, 1] = 255

        blue = np.zeros((dims[1], dims[0], 3), np.uint8)
        blue[:, :, 0] = 255

        frames = [green, blue]
        yield frames
