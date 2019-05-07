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

from abc import abstractmethod, ABCMeta
from typing import List

from core.scene.generator import Generator
from core.common.segment import Segment
from core.scene.scene import Scene
from core.common.evaluation_resources import EvaluationResources


class GeneratorStatic(Generator):

    def __init__(self, segments: List[Segment], interval=5.0):
        self.segments = segments
        self.interval = interval

    def generate_scenes(self):
        scene_list = list()
        scene = Scene()
        for segment in self.segments:
            scene.add_segment(segment)
            if scene.get_interval() > self.interval:
                seg = scene.segments.pop()
                scene_list.append(scene)
                scene = Scene()
                scene.add_segment(seg)
        if scene_list[-1] != scene:
            scene_list.append(scene)
        return scene_list


class GeneratorScore(Generator):

    def __init__(self, segments: List[Segment], windows_size=30):
        self.segments = segments
        self.windows_size = windows_size

    def generate_scenes(self):

        scene = Scene()
        scene_list = list()
        for i, segment in enumerate(self.segments):
            if i >= self.windows_size and i < len(self.segments) - 1:
                if self._is_local_minimum(i):
                    scene_list.append(scene)
                    scene = Scene()
            scene.add_segment(segment)
        scene_list.append(scene)
        return scene_list

    def _is_local_minimum(self, index) -> bool:
        p1 = p2 = p3 = float()

        for i in range(index - self.windows_size + 1, index + 1):
            p1 += self.segments[i - 1].get_score()
            p2 += self.segments[i].get_score()
            p3 += self.segments[i + 1].get_score()
        if p2 - p1 <= 0 and p3 - p2 > 0:
            return True
        else:
            return False
