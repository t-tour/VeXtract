import os
import sys
__root = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + (os.sep + '..') * (
        len(os.path.dirname(os.path.abspath(__file__)).split(os.sep)) -
        os.path.dirname(os.path.abspath(__file__)).split(os.sep).index(
            'VeXtract'
        ) - 1
    )) + os.sep
sys.path.append(__root)
_ROOT = __root

from helper import logger
log = logger.Logger(__name__)

from pathlib import Path

from core.scene.generators import GeneratorStatic, GeneratorScore
from core.common.segment import Segment
from core.common.evaluation_resources import EvaluationResources

# 一般來說 segment 不會這麼大，測試所以忽略scene是由更多小segment組成的


def init_generatorstatic():
    segments = [Segment((i, i + 1)) for i in range(5)]
    g = GeneratorStatic(segments, interval=2.0)
    return g


def test_generatorstatis_geneate_scenes():
    g = init_generatorstatic()
    scenes = g.generate_scenes()
    assert len(scenes) == 3
    assert scenes[1].get_time() == (2, 4)


def init_generatorscore():
    segments = list()
    for i in range(500):
        seg = Segment((i / 10.0, (i + 1) / 10.0))
        seg.add_score(i % 100)
        segments.append(seg)
    g = GeneratorScore(segments)
    return g


def test_generatorscore_generate_scenes():
    g = init_generatorscore()
    scene = g.generate_scenes()
    assert len(scene) == 5
    assert scene[1].get_time() == (12.9, 22.9)


def test_generatorscore_local_minimum():
    segments = list()
    for i in range(10):
        seg = Segment((i, i + 1))
        seg.add_score(i % 5)
        segments.append(seg)
    g = GeneratorScore(segments, windows_size=4)
    asserted_list = [g._is_local_minimum(i)for i in range(4, 9)]

    assert asserted_list == [False, False, False, False, True]
