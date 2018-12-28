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

from core.scene.generators import GeneratorComment, GeneratorStatic, GeneratorVAD, GeneratorScore
from core.common.segment import Segment
from core.common.evaluation_resources import EvaluationResources

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


def init_generatorstatic():
    segments = [Segment((i, i + 1), False) for i in range(5)]
    g = GeneratorStatic(segments, interval=2.0)
    return g


def test_generatorstatis_geneate_scenes():
    g = init_generatorstatic()
    scenes = g.generate_scenes()
    assert len(scenes) == 3
    assert scenes[1].get_time() == (2, 4)


def init_generatorcomment():
    comment1 = {"text": "te", "sec": 4.7}
    comment2 = {"text": "te", "sec": 15.5}
    comment3 = {"text": "te", "sec": 16}
    comment4 = {"text": "te", "sec": 16.5}
    comment5 = {"text": "te", "sec": 17.5}
    comments = [comment1, comment2, comment3, comment4, comment5]
    er = EvaluationResources(comments)
    segments = [Segment((i / 10.0, (i + 1) / 10.0), False)
                for i in range(500)]  # 50 個 segment 0 ~ 50 秒
    g = GeneratorComment(segments, er)
    return g


def test_generatorcomment_generate_scenes():
    g = init_generatorcomment()
    scenes = g.generate_scenes()
    assert len(scenes) == 5
    assert scenes[1].get_time() == (3.2, 6.2)


def init_generatorscore():
    segments = list()
    for i in range(500):
        seg = Segment((i / 10.0, (i + 1) / 10.0), False)
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
        seg = Segment((i, i + 1), False)
        seg.add_score(i % 5)
        segments.append(seg)
    g = GeneratorScore(segments, windows_size=4)
    asserted_list = [g._is_local_minimum(i)for i in range(4, 9)]

    assert asserted_list == [False, False, False, False, True]
