from utilities.video import *
from utilities.bg_video import *
from utilities.box_video import *


vc = VideoCreator((960, 1080), 2)
vc.export(box_moving(30, (960, 1080), 20))
