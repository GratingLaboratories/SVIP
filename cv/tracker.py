import numpy as np
import cv2


def onMouse(event, x, y, flag, param):
    if isinstance(param, tracker) == False:
        return
    if event == cv2.EVENT_LBUTTONDOWN:
        param.changePos(x / 2, y / 2)


class eye():
    def __init__(self, width, x=0, y=0):
        self.x = x
        self.y = y
        self.width = width
        self.prev = (x, y)


class Region:
    def __init__(self):
        self.start = []
        self.end = []


class tracker():
    def __init__(self, bact, max_x, max_y):
        self.bact = bact
        self.isinited = True
        self.outofFocus = False
        self.isLost = True
        self.xrange = [0, 0]
        self.yrange = [0, 0]
        self.max_x = max_x
        self.max_y = max_y
        self.ischangeing = False
        self.contrast_prev = 0
        self.dire_up = False
        self.isgreat = True
        self.eye_cascade = cv2.CascadeClassifier('../resources/haarcascade_eye.xml')
        self.retry = 0

    def changePos(self, x, y):
        self.bact.x = x
        self.bact.y = y
        self.bact.prev = (x, y)
        self.isLost = False
        self.outofFocus = False
        self.ischangeing = True
        self.setRange()
        self.ischangeing = False
        self.dynamic = True

    def update(self, frame):
        if self.isinited == False or self.isLost == True or self.ischangeing == True:
            return 0


        if self.dynamic:
            x, y = self.bact.x, self.bact.y
            # frame = np.ones(frame.shape) * 255 - frame
            self.bact.x += self.bact.x - self.bact.prev[0]
            self.bact.y += self.bact.y - self.bact.prev[1]
            self.bact.prev = (x, y)
        self.setRange()

        ylow = self.yrange[0]
        yhigh = self.yrange[1]
        xlow = self.xrange[0]
        xhigh = self.xrange[1]

        region = frame[ylow : yhigh, xlow: xhigh]

        region = np.array(region, dtype='uint8')
        # cv2.imshow('small', region)
        eyes = self.eye_cascade.detectMultiScale(region, 1.1, 4, minSize=(20, 20), maxSize=(50, 50))

        if len(eyes) > 0:
            self.retry = 0
            posx, posy, ew, eh = next(iter(eyes))
            self.bact.width = int(max(max(ew, eh), 10))
            posx += ew / 2
            posy += eh / 2
            self.bact.x = self.xrange[0] + posx
            self.bact.y = self.yrange[0] + posy
            self.dynamic = True
        else:
            if self.retry > 5:
                region = np.ones(region.shape) * 255 - region
                res = np.where(region >= region.max() - 3)
                resy = res[0]
                resx = res[1]
                posx = resx.mean()
                posy = resy.mean()
                self.bact.x = self.xrange[0] + posx
                self.bact.y = self.yrange[0] + posy
            else:
                self.retry += 1
            self.dynamic = False
            # self.setRange()
        # res = np.where(region >= region.max() - 3)
        # resy = res[0]
        # resx = res[1]
        # posx = resx.mean()
        # posy = resy.mean()
        # self.isLost = False
        return self.bact.x, self.bact.y

    def setRange(self):
        x = int(self.bact.x)
        y = int(self.bact.y)

        if x - self.bact.width > 0:
            self.xrange[0] = x - self.bact.width
        else:
            self.isLost = True
            return

        if x + self.bact.width < self.max_x:
            self.xrange[1] = x + self.bact.width
        else:
            self.isLost = True
            return

        if y - self.bact.width > 0:
            self.yrange[0] = y - self.bact.width
        else:
            self.isLost = True
            return

        if y + self.bact.width < self.max_y:
            self.yrange[1] = y + self.bact.width
        else:
            self.isLost = True
            return

if __name__ == '__main__':
    font = cv2.FONT_HERSHEY_SIMPLEX
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    y, x, channel = np.shape(frame)
    track = tracker(eye(30), x , y)
    cv2.namedWindow('test')
    cv2.namedWindow('small')
    cv2.setMouseCallback('test', onMouse, track)
    contrast = 0

    while(1):
        ret, frame = cap.read()
        if frame is None:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        track.update(gray)

        if track.isLost:
            cv2.putText(frame, "Bacterium lost", (10, 200), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "2D fixed", (10, 200), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.rectangle(frame, (track.xrange[0], track.yrange[0]), (track.xrange[1], track.yrange[1]), (255, 0, 0), 3)

        cv2.putText(frame, "x=%.2f, y=%.2f" % (track.bact.x, track.bact.y), (10, 50), font, 0.5,
                        (255, 255, 255), 1, cv2.LINE_AA)
        frame = cv2.resize(frame, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
        cv2.imshow('test', frame)
        if cv2.waitKey(30) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
    cap.release()