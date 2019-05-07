import os
import sys
__root = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + (os.sep + '..') * (
        len(os.path.dirname(os.path.abspath(__file__)).split(os.sep))
        - os.path.dirname(os.path.abspath(__file__)).split(os.sep).index(
            'VeXtract'
        ) - 1
    )) + os.sep
sys.path.append(__root)
_ROOT = __root

from helper import logger
log = logger.Logger(__name__)

from pathlib import Path

from core.video import Video
from core.scene.scene import Scene, Segment


PATH = Path(_ROOT, "test", "test_file", "3s_interval_vocal.wav")

first_scene = Scene()
first_scene.add_segment(Segment((0.0, 1.0)))
second_scene = Scene()
second_scene.add_segment(Segment((1.0, 5.0)))
third_scene = Scene()
third_scene.add_segment(Segment((10.0, 20.0)))

scenes_list = [first_scene, second_scene, third_scene]

