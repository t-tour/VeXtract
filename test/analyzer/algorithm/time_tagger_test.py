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
from crawler.bilibili import bilibili_info
AVNUMBER = "av23315808"
AVJSON_PATH = os.path.join(
    __root, "test\\test_file\\{av}.json".format(av=AVNUMBER))
VIDEO = os.path.join(__root, "test\\test_file\\{av}.mp4".format(av=AVNUMBER))

def test__generate_segments():
    log.i('Strat test__generate_segments.')
    a = time_tagger._generate_segments(VIDEO)
    assert_total_length = video_algorithm.get_video_length(VIDEO)
    total_length = 0
    for time in a:
        total_length += time[1] - time[0]
    assert assert_total_length == total_length


def test_wanted_length():
    log.i('Start test_wanted_length.')
    a = bilibili_info.Bilibili_file_info.load(AVJSON_PATH)
    asserted_total_length = 15.5
    tagged_list = time_tagger.count_wanted_length(
        asserted_total_length, VIDEO, real_time_comments=a.comments[a.cid[0]])
    total_length = 0
    for tagged in tagged_list:
        total_length += tagged[1] - tagged[0]
    assert asserted_total_length >= total_length