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

from analyzer.algorithm import segment_generator
from analyzer.algorithm import video_algorithm

VIDEO = os.path.join(__root, "test", "test_file", "av23315808.mp4")

def test_generate_segments():
    log.i('Strat test_generate_segments.')
    a = segment_generator.generate_segments(VIDEO)
    assert_total_length = video_algorithm.get_video_length(VIDEO)
    total_length = 0
    for time in a:
        total_length += time[1] - time[0]
    assert assert_total_length == total_length