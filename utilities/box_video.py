import cv2
import numpy as np


def box_moving(time, dims, fps, dense=50, length=80, vel=10, omega=0.01, A=1, far=6, eye_d=0.5):
    width, height = dims
    blank_img = np.zeros((height, width, 3), np.uint8)

    # Generate base mesh
    for i in list(np.linspace(0, width, dense)):
        cv2.line(blank_img, (int(i), 0), (int(i), height), (115, 85, 47), 2)

    for i in list(np.linspace(0, height, dense)):
        cv2.line(blank_img, (0, int(i)), (height, int(i)), (115, 85, 47), 2)
    
    def projection():
        distance = far + nextPos[2]
        delta = nextPos[2] * eye_d / distance
        return delta

    pos = np.array([width / 2, height / 2, 0])
    direction = np.random.random((2))
    direction /= np.linalg.norm(direction)
    velocity = direction * vel
    velocity = np.append(velocity, 0)

    for i in range(time * fps):
        nextPos = pos + velocity
        if width < length / 2 + nextPos[0]:
            nextPos[0] = width - length / 2 - (nextPos[0] + length / 2 - width)
            velocity[0] = -velocity[0]
        elif nextPos[0]- length / 2 < 0:
            nextPos[0] = length - nextPos[0]
            velocity[0] = -velocity[0]

        if nextPos[1] + length / 2 > height:
            nextPos[1] = height - length / 2 - (nextPos[1] + length / 2 - height)
            velocity[1] = -velocity[1]
        elif nextPos[1] - length / 2 < 0:
            nextPos[1] = length - nextPos[1]
            velocity[1] = -velocity[1]

        nextPos[2] = A * np.sin(2 * np.pi * omega * i) + 1
        delta = projection()

        pos_lr = [[nextPos[0] - delta, nextPos[1]], [nextPos[0] + delta, nextPos[1]]]
        frames = []
        for center in pos_lr:
            meshed = blank_img.copy()
            lu = (int(center[0] - length / 2), int(center[1] - length / 2))
            rd = (int(center[0] + length / 2), int(center[1] + length / 2))
            ld = (int(center[0] - length / 2), int(center[1] + length / 2))
            ru = (int(center[0] + length / 2), int(center[1] - length / 2))
            pts = np.array([lu, ld, rd, ru], np.int32)
            cv2.fillPoly(meshed, np.array([pts], np.int32), (128, 0, 0))
            frames.append(meshed)
        
        pos = nextPos

        yield frames
