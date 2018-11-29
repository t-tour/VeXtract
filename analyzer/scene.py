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

    def __init__(self):
        self.segments = list()

    def add_segment(self, segment):
        self.segments.append(segment)

    def is_accept_vocal(self):
        amount = 0
        for segment in self.segments:
            if segment.isvocal:
                amount += 1
        return amount > 0.5

    def istooshort(self):
        if len(self.segments) == 0:
            return True
        return (self.segments[-1].get_end_time() - self.segments[0].get_start_time()) < 5

    def istoolong(self):
        if len(self.segments) == 0:
            return False
        return (self.segments[-1].get_end_time() - self.segments[0].get_start_time()) > 60

    def get_avg_score(self):
        amount = 0
        for segment in self.segments:
            amount += segment.score
        return amount / len(self.segments)

    def get_cut_time(self):
        return (self.segments[0].get_start_time(), self.segments[-1].get_end_time())
