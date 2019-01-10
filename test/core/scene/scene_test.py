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

from core.scene.scene import Scene
from core.common.segment import Segment

SCENE = Scene()
SCENE.add_segment(Segment((2,15.5), False))
SCENE.add_segment(Segment((25,30), True))

SCENE2 = Scene()
SCENE2.add_segment(Segment((11,15.5), False))
SCENE2.add_segment(Segment((25,27), True))

SCENE_LIST = [SCENE, SCENE2]

def test_scene_str():
    assert str(SCENE) == "(2, 30)"

def test_repr_():
    assert str(SCENE_LIST) == "[(2, 30), (11, 27)]"
