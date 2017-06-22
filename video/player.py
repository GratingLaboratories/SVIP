import cv2
import numpy as np
import logging


class VideoPlayer:
    def __init__(self, channel_num, src, dims, full_screen=True):
        self.channel_num = channel_num
        self.src = src
        self.dims = dims
        cv2.namedWindow('Grating Player')

    def play(self, mask_iter, ppl, export=False):
        cap = cv2.VideoCapture(self.src)

        def resize_with_padding(img, target_dim):
            height, width, channels = img.shape
            t_width, t_height = target_dim
            w_ratio = t_width / width
            h_ratio = t_height / height
            ratio = min(w_ratio, h_ratio)
            img = cv2.resize(img, None, fx=ratio, fy=ratio)
            if w_ratio < h_ratio:
                tmp = np.zeros((self.dims[1], img.shape[1], 3), np.uint8)
                start = int((self.dims[1] - int(round(ratio * s_height))) / 2)
                tmp[start : start + img.shape[0], :] = img
                img = tmp
            return img

        indicator = list(np.int32(np.zeros(self.dims[0])))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            s_height, s_width, channel = frame.shape
            try:
                mask = next(mask_iter)
            except StopIteration:
                logging.critical('Core engine failed to supply mask, player corrupted')
                return None

            # Div frame into frames
            starts = list(np.int32(np.linspace(0, frame.shape[1], self.channel_num + 1)))
            head = starts[0: -1]
            tail = starts[1:]
            sub_frames = []
            for i, j in zip(head, tail):
                tmp = frame[:, i: j]
                sub_frames.append(cv2.resize(tmp, None, fx=1 / self.channel_num, fy=1))

            offset = 0
            padding = False
            tailer = ppl - int(ppl)
            mask = list(mask)
            for i in range(len(indicator)):
                j = (i + offset) % int(ppl)
                if padding:
                    padding = False
                    indicator[i] = 0
                    offset -= 1
                    tailer -= 1
                elif j >= len(mask) - 1:
                    if np.abs(tailer - 1) < 0.1 or tailer >= 1:
                        padding = True
                    indicator[i] = mask[j]
                    tailer += ppl - int(ppl)
                else:
                    indicator[i] = mask[j]

            widthes = []
            for marker in range(self.channel_num):
                widthes.append(indicator.count(marker + 1))
            
            layers = []
            for i in range(len(sub_frames)):
                img = resize_with_padding(sub_frames[i], (widthes[i], self.dims[1]))
                layers.append(img)

            # for i in range(2):
                # cv2.imshow(str(i), sub_frames[i])
                # print(i, indicator.count(i + 1))

            # Build new frame
            new_frame = np.zeros((self.dims[1], self.dims[0], 3), np.uint8)
            pointers = [0, ] * self.channel_num
            for i in range(len(indicator)):
                index = indicator[i] - 1
                if index != -1:
                    try:
                        new_frame[:, i] = layers[index][:, pointers[index]]
                    except IndexError as e:
                        # print(e)
                        pass
                    pointers[index] += 1
                else:
                    continue

            if export:
                yield new_frame
            else:
                cv2.imshow('Grating Player', new_frame)
                cv2.waitKey(20)
