from utilities.video import *
from utilities.bg_video import *
from utilities.box_video import *
from video.player import *
from core import *

# vc = VideoCreator((1920, 1080), 2)
# vc.export(box_moving(60, (1920, 1080), 30), fps=30, filename='output1.avi')
#
player = VideoPlayer(2, 'output1.avi', (1920, 1080))
save_iter = player.play(static_mask([0, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 0]), 13.41, export=False)

next(save_iter)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('box.avi', fourcc, 30, (1920, 1080))
# for frame in save_iter:
#     out.write(frame)
# out.release()