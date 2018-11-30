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

from analyzer.segment import Segment


class Scene(object):

    segments: List[Segment]

    def __init__(self, minimum_length, maximum_length):
        self.segments = list()
        self.minimum_length = minimum_length
        self.maximum_length = maximum_length

    def add_segment(self, segment):
        self.segments.append(segment)

    def is_accept_vocal(self):
        amount = 0
        for segment in self.segments:
            if segment.isvocal:
                amount += 1
        return amount > 0.5

    def is_have_segment(self):
        return len(self.segments) != 0

    def get_interval(self):
        return self.segments[-1].get_end_time() - self.segments[0].get_start_time()

    def istooshort(self):
        if not self.is_have_segment():
            return True
        return self.get_interval() < self.minimum_length

    def istoolong(self):
        if not self.is_have_segment:
            return False
        return self.get_interval() > self.maximum_length

    def get_avg_score(self):
        amount = 0
        for segment in self.segments:
            amount += segment.score
        return amount / len(self.segments)

    def get_cut_time(self):
        return (self.segments[0].get_start_time(), self.segments[-1].get_end_time())

    def copy(self):
        return Scene(self.minimum_length, self.maximum_length)
