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

from pathlib import Path
import math

from matplotlib import pyplot as plt

from analyzer.video.video import Video
from analyzer.evaluation_resources import EvaluationResources
from crawler.bilibili.bilibili_info import Bilibili_file_info

PATH = Path(__root, "file", "crawler", "bLjirHrCdbs.mp4")
JSON = os.path.join(__root, "test", "test_file", "av23315808.json")

def test_video_construct():
    video = Video(PATH)
    video.generate_scenes()
    b_info = Bilibili_file_info.load(JSON)
    er = EvaluationResources(b_info.comments[b_info.cid[0]]) 
    video.set_evaluation_resources(er)
    video.evaluate()
    print()
    