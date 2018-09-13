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

from analyzer.algorithm import time_tagger
from analyzer.algorithm import video_algorithm

VIDEO = os.path.join(__root, "test\\test_file\\analyzer_file.mp4")

def test__generate_segments():
    log.i('Strat test__generate_segments.')
    a = time_tagger.__generate_segments(VIDEO)
    assert_total_length = video_algorithm.get_video_length(VIDEO)
    total_length = 0
    for time in a:
        total_length += time[1] - time[0]
    assert assert_total_length == total_length