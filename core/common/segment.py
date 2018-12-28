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

from helper import logger
log = logger.Logger(__name__)


class Segment(object):

    def __init__(self, time, isvocal: bool):
        self.time = time
        self.score = 0.0
        self.isvocal = isvocal

    def get_start_time(self):
        return self.time[0]

    def get_end_time(self):
        return self.time[1]

    def get_interval(self):
        return self.time[1] - self.time[0]

    def add_score(self, point: float):
        self.score += point

    def get_score(self):
        return self.score

    # @staticmethod
    # def concat(segment1: Segment, segment2: Segment):
    #     new_start_timeat = float()
    #     new_end_timeat = float()
    #     if segment1.get_start_time() == segment2.get_end_time():
    #         new_start_timeat = segment2.get_start_time()
    #         new_end_timeat = segment1.get_end_time()
    #     elif segment2.get_start_time() == segment1.get_end_time():
    #         new_start_timeat = segment1.get_start_time()
    #         new_end_timeat = segment2.get_end_time()
    #     else:
    #         raise Exception("unSupport segment pair.")
    #     return Segment((new_start_timeat, new_end_timeat))
