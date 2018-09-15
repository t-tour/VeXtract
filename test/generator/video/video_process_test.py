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

filename = os.path.join(__root, "test\\test_file", "test_video.mp4")
output_location = os.path.join(__root, "test\\test_file\\test_temp")
output_name = "test_video_666.mp4"
ouput = os.path.join(output_location, output_name)


def test_video_process_with_temp():
    log.i('start video_process_with_temp_test.')
    shutil.rmtree(output_location, ignore_errors=True)
    split_list = [(0.0, 4.0), (6.0, 10.0), (13.0, 17.0), (24.0, 28.0)]
    """
    split_list = [(115.0, 120.0), (425.0, 430.0), (750.0, 755.0), (755.0, 760.0),
                  (760.0, 765.0), (830.0, 835.0), (930.0, 935.0), (985.0, 990.0),
                  (990.0, 995.0), (1135.0, 1140.0), (1140.0, 1145.0), (1585.0, 1590.0)]
    """
    """
    split_list = [(425.0, 430.0), (750.0, 755.0),
                  (760.0, 765.0), (830.0, 835.0), (930.0, 935.0),
                  (990.0, 995.0), (1140.0, 1145.0)]
    """
    """"
    split_list = [(0.0, 5.0), (15.0, 20.0), (45.0, 50.0), (55.0, 60.0),
                  (75.0, 80.0), (85.0, 90.0), (100.0, 105.0), (115.0, 120.0),
                  (135.0, 140.0), (155.0, 160.0), (175.0, 180.0), (195.0, 200.0)]
    """
    video_process.video_process(
        filename, split_list, True, output_location, output_name)
    assert os.path.exists(ouput) == True
    shutil.rmtree(ouput, ignore_errors=True)
    video_name = os.path.basename(filename).split(".")[0]
    video_type = os.path.basename(filename).split(".")[-1]
    temp_name = video_name+"_temp"
    for i in range(len(split_list)):
        ouput_temp = os.path.join(
            output_location, temp_name, video_name+"-"+str(i)+"."+video_type)
        assert os.path.exists(ouput_temp) == True
        shutil.rmtree(ouput_temp, ignore_errors=True)
    shutil.rmtree(output_location, ignore_errors=True)


def test_video_encoding():
    log.i('start video_encoding_test.')
    shutil.rmtree(output_location, ignore_errors=True)
    filename = os.path.join(__root, "test\\test_file", "test_video.mp4")
    output_name = "test_video_666.flv"
    ouput = os.path.join(output_location, output_name)
    video_process.video_encoding(filename, output_location, output_name)
    assert os.path.exists(ouput) == True
    shutil.rmtree(ouput, ignore_errors=True)
    shutil.rmtree(output_location, ignore_errors=True)
