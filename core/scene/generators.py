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

from abc import abstractmethod, ABCMeta
from typing import List

from core.scene.generator import Generator
from core.common.segment import Segment
from core.scene.scene import Scene


class GeneratorVAD(Generator):

    def __init__(self, segments: List[Segment]):
        self.segments = segments
        self.scenes = list()

    def generate_scenes(self):
        # TODO: 重構需求現階段先排除segment震盪問題，往後可能需要語者分析與更穩定的VAD方法
        scene = Scene()

        for segment in self.segments:
            if len(scene.segments) == 0:
                scene.add_segment(segment)
            segment_is_vocal = 1 if segment.isvocal else 0
            if scene.get_vocal_avg() == segment_is_vocal:
                scene.add_segment(segment)
            else:
                self.scenes.append(scene)
                scene = Scene()
                scene.add_segment(segment)
        # add the last one scene
        self.scenes.append(scene)
        return self.scenes

    # 現在先不需要，假設VAD穩定scenes不會只有單個segment造成時間過短
    # def _concat_scenes(self):
    #     new_scenes_list = list()
    #     compare_scenes_list = list()

    #     for add_scene in self.scenes:
    #         compare_scenes_list.append(add_scene)
    #         amount = 0
    #         for scene in compare_scenes_list:
    #             amount += scene.get_interval()
    #         if amount > scene.minimum_length:
    #             new_scenes_list.append(Scene.join_scenes(compare_scenes_list))
    #             compare_scenes_list = list()
    #         else:
    #             continue
    #     if len(compare_scenes_list) != 0:
    #         last_scene = new_scenes_list.pop()
    #         compare_scenes_list.insert(0, last_scene)
    #         new_last_scene = Scene.join_scenes(compare_scenes_list)
    #         new_scenes_list.append(new_last_scene)
    #     self.scenes = new_scenes_list


class GeneratorComment(Generator):
    def generate_scenes(self):
        return super().generate_scenes()


class GeneratorStatic(Generator):
    def generate_scenes(self):
        return super().generate_scenes()

