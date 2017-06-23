import cv2
import numpy as np
import matplotlib.pyplot as plt


class VideoCreator:
    def __init__(self, dims, channel_num=2):
        """
            dims: (width, height) of 1 frame
            channel_num: The amount of frames you want to combine
        """
        self.channel_num = channel_num
        self.dims = dims

    def merge(self, frames):
        # Create a blank frame
        width, height = self.dims

        # Pre-process
        if len(frames) < self.channel_num:
            padding = np.zeros(height, width * (self.channel_num - len(frames)))
            frames.append(padding)
        elif len(frames) > self.channel_num:
            frames = frames[0:self.channel_num]

        frame = np.hstack(frames)
        return frame

    def export(self, src, fps=20.0, filename='output1.avi', codec='XVID'):
        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename, fourcc, fps, (self.dims[0] * self.channel_num, self.dims[1]))

        for frames in src:
            frame = self.merge(frames)
            # print(frame.shape)
            # cv2.imshow('image', frame)
            # cv2.waitKey(0)
            out.write(frame)

        out.release()
        cv2.destroyAllWindows()