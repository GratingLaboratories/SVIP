from utilities.video import *
from utilities.bg_video import *


vc = VideoCreator((960, 1080), 2)
vc.export(bg_generator(5, (960, 1080)))
