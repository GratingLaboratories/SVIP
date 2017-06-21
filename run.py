from utilities.video import *
from utilities.bg_video import *
from utilities.box_video import *
from video.player import *
from core import *

# vc = VideoCreator((960, 1080), 2)
# vc.export(bg_generator(30, (960, 1080), 30), fps=30)

player = VideoPlayer(2, 'output1.avi', (960, 540))
player.play(static_mask([1, 1, 2, 2]), 4.32)
