import cv2
import numpy as np
import logging
import time
from cv.tracker import *

class EyeTracker:
    def __init__(self, face_xml='resources/haarcascade_frontalface_default.xml',
                 eye_xml='./resources/haarcascade_eye.xml', device=0, show=False):
        self.eyes = [np.zeros(2), np.zeros(2)]
        self.lost = True
        self.initedF = False
        self.face_xml = face_xml
        self.eye_xml = eye_xml
        self.face_cascade = cv2.CascadeClassifier(self.face_xml)
        self.eye_cascade = cv2.CascadeClassifier(self.eye_xml)
        self.cap = cv2.VideoCapture(device)
        self.eye_sets = {'left': [], 'right': [], 'size': []}
        self.tried = 0
        self.success = 0
        self.show = show
        if self.show:
            cv2.namedWindow("Tracker")

        self.reCali = False

    def calibration(self, try_times=5, max_time=5, add_rect=False):
        start_time = time.time()
        logging.info("Starting eye tracker calibration")
        self.success = 0
        self.tried = 0
        self.eye_sets = {'left': [], 'right': [], 'size': []}
        while True:
            ret, frame = self.cap.read()
            if not ret:
                logging.error("Camera faield")
                return None

            self.tried += 1
            if self.success >= try_times or (time.time() - start_time) > max_time:

                if self.success >= try_times:
                    self.lost = False
                    self.initedF = False
                else:
                    self.initedF = True
                    return False
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                if add_rect:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                roi_gray = gray[y: y + h, x: x + w]
                roi_color = frame[y: y + h, x: x + w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                eyes_list = []
                for (ex, ey, ew, eh) in eyes:
                    eyes_list.append((ex + x, ey + y, ew, eh))
                    if add_rect:
                        cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 255), 2)

                if len(eyes_list) == 2:
                    self.success += 1
                    x0, x1 = eyes_list[0][0], eyes_list[1][0]
                    eye0, eye1 = eyes_list[0], eyes_list[1]
                    eye0 = np.array([eye0[0] + eye0[2] / 2, eye0[1] + eye0[3] / 2])
                    eye1 = np.array([eye1[0] + eye1[2] / 2, eye1[1] + eye1[3] / 2])
                    self.eye_sets['left'].append(eye0 if x0 > x1 else eye1)
                    self.eye_sets['right'].append(eye1 if x0 > x1 else eye0)
                    self.eye_sets['size'].append(max(eyes_list[0][2], eyes_list[0][3], eyes_list[1][2], eyes_list[1][3]))

            if self.show:
                cv2.imshow("Tracker", frame)
                if cv2.waitKey(30) & 0xFF == 27:
                    break

        return True

    def track(self, min_distance=400, max_distance=20000, add_rect=True, font=cv2.FONT_HERSHEY_SIMPLEX):
        print("Calibration")
        result = self.calibration(add_rect=True, max_time=5)
        print("Calibrated... result=", result, self.success)
        if not result:
            logging.warning('Failed to calibrate tracking program, exiting...')
            return None

        ret, frame = self.cap.read()
        if not ret:
            logging.error("Camera faield")
            return None

        init_size = int(round(np.average(np.array(self.eye_sets['size']))))
        l_pos = np.average(np.array(self.eye_sets['left']), axis=0)
        r_pos = np.average(np.array(self.eye_sets['right']), axis=0)

        height, width, channel = frame.shape
        l_tracker = Tracker(Eye(init_size), width, height)
        r_tracker = Tracker(Eye(init_size), width, height)

        print(l_pos, r_pos)
        # Set init position
        l_tracker.change_pos(int(round(l_pos[0])), int(round(l_pos[1])))
        r_tracker.change_pos(int(round(r_pos[0])), int(round(r_pos[1])))

        distance = lambda A, B: (A.x - B.x) ** 2 + (A.y - B.y) ** 2
        re_cali = False
        while True:
            ret, frame = self.cap.read()
            if not ret:
                return None
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            l_tracker.update(gray, dynamic=True)
            r_tracker.update(gray, dynamic=True)

            if distance(l_tracker.bact, r_tracker.bact) < min_distance or distance(l_tracker.bact, r_tracker.bact) > max_distance:
                re_cali = True

            if l_tracker.isLost or r_tracker.isLost:
                cv2.putText(frame, "Eyes lost", (10, 200), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
                re_cali = True
            else:
                cv2.putText(frame, "2D fixed", (10, 200), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.rectangle(frame, (l_tracker.xrange[0], l_tracker.yrange[0]),
                              (l_tracker.xrange[1], r_tracker.yrange[1]), (0, 255, 64), 3)
                cv2.rectangle(frame, (r_tracker.xrange[0], r_tracker.yrange[0]),
                              (r_tracker.xrange[1], r_tracker.yrange[1]), (64, 255, 0), 3)

            if re_cali:
                result = self.calibration(add_rect=True, max_time=5)
                if result:
                    l_pos = np.average(np.array(self.eye_sets['left']), axis=0)
                    r_pos = np.average(np.array(self.eye_sets['right']), axis=0)
                    l_tracker.change_pos(int(round(l_pos[0])), int(round(l_pos[1])))
                    r_tracker.change_pos(int(round(r_pos[0])), int(round(r_pos[1])))
                    re_cali = False
                else:
                    pass

            if self.show:
                cv2.imshow('Tracker', frame)
                if cv2.waitKey(30) & 0xFF == 27:
                    break

    def update(self):
        pass


def main():
    tracker = EyeTracker(show=True)
    # result = tracker.calibration(add_rect=True)
    # print(result)
    # print(tracker.initedF, tracker.success)
    tracker.track()

if __name__ == '__main__':
    main()
