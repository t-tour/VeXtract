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

from typing import List


class RealTimeComment():

    def __init__(self, timeat, text):
        self.timeat = timeat
        self.text = text

    def get_text(self):
        return self.text

    def get_timeat(self):
        return float(self.timeat)


class EvaluationResources(object):

    def __init__(self, real_time_comments):
        self.real_time_comments = list()
        for comment in real_time_comments:
            timeat = comment['sec']
            text = comment['text']
            self.real_time_comments.append(RealTimeComment(timeat, text))
        self.real_time_comments = sorted(
            self.real_time_comments, key=lambda foo: foo.get_timeat())

    def is_real_time_comment_exist(self):
        return len(self.real_time_comments) > 0

    def get_real_time_comments(self) -> List[RealTimeComment]:
        return self.real_time_comments
