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

from core.scene.generators import GeneratorComment, GeneratorStatic, GeneratorVAD
from core.common.segment import Segment

# 一般來說 segment 不會這麼大，測試所以忽略scene是由更多小segment組成的
def init_generatorVAD():
    s1 = Segment((0, 15), False)
    s2 = Segment((15, 30), True)
    s3 = Segment((30, 45), True)
    s4 = Segment((45, 60), False)
    s5 = Segment((60, 75), False)
    segments = [s1, s2, s3, s4, s5]
    g = GeneratorVAD(segments)
    return g


def test_generatorVAD_geneate_scenes():
    g = init_generatorVAD()
    scenes = g.generate_scenes()
    scene = scenes[1]
    assert len(scenes) == 3
    assert scene.get_time() == (15.0, 45.0)
