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

from helper import logger
log = logger.Logger(__name__)

from typing import List

from core.common.segment import Segment


class Scene(object):

    segments: List[Segment]

    def __init__(self):
        self.segments = list()

    def add_segment(self, segment):
        self.segments.append(segment)

    def get_vocal_avg(self):
        amount = 0
        for segment in self.segments:
            if segment.isvocal:
                amount += 1
        avg = amount / len(self.segments)
        return avg

    def is_have_segment(self):
        return len(self.segments) != 0

    def get_interval(self):
        return self.segments[-1].get_end_time() - self.segments[0].get_start_time()

    def get_time(self):
        self.time = (self.segments[0].get_start_time(), self.segments[-1].get_end_time())
        return self.time

    def get_avg_score(self):
        amount = 0
        for segment in self.segments:
            amount += segment.score
        self.avg_score = amount / len(self.segments)
        return amount / len(self.segments)

    def get_startat(self):
        return self.segments[0].get_start_time()

    @staticmethod
    def join_scenes(scenes_list: list):
        if len(scenes_list) == 1:
            return scenes_list[0]
        first_scene = scenes_list[0]
        for i in range(1, len(scenes_list)):
            for segment in scenes_list[i].segments:
                first_scene.add_segment(segment)
        return first_scene

    def __str__(self):
        return str(self.get_time())

    def __repr__(self):
        return self.__str__()
