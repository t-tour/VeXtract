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

import shutil

import pytest

from generator.video import video_process

filename = os.path.join(__root, "file", "14391479.flv")
output_location = os.path.join(__root, "file", "generator")
output_name = "666.flv"
ouput = os.path.join(output_location, output_name)


def test_video_process_with_temp():
    log.i('start video_process_test.')
    split_list = [(115.0, 120.0), (425.0, 430.0), (750.0, 755.0), (755.0, 760.0),
                  (760.0, 765.0), (830.0, 835.0), (930.0, 935.0), (985.0, 990.0),
                  (990.0, 995.0), (1135.0, 1140.0), (1140.0, 1145.0), (1585.0, 1590.0)]
    video_process.video_process(
        filename, split_list, True, output_location, output_name)
    ouput_temp = os.path.join(output_location, "temp")
    assert os.path.exists(ouput) == True
    assert os.path.exists(ouput_temp) == True
