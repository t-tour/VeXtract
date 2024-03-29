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

from generator.video import video_split
from analyzer.algorithm import video_algorithm

filename = os.path.join(__root, "test\\test_file", "test_video.mp4")
output_location = os.path.join(__root, "test\\test_file\\test_temp")
output_name = "test_video_666.mp4"
ouput = os.path.join(output_location, output_name)


def test_split_by_frame():
    log.i('start split_by_frame_test.')
    video_name = os.path.basename(filename)
    video_name = video_name.split(".")[0]
    temp_name = video_name+"_frames"
    shutil.rmtree(output_location, ignore_errors=True)
    start_time = 5
    frame_number = 30
    video_split.split_by_frame(
        filename, start_time, frame_number, output_location)
    for i in range(1, frame_number+1):
        frame_name = "%s-%s.jpg" % (video_name, i)
        ouput = os.path.join(output_location, temp_name, frame_name)
        assert os.path.exists(ouput) == True
        shutil.rmtree(ouput, ignore_errors=True)
    shutil.rmtree(output_location, ignore_errors=True)


def test_split_by_manifest():
    log.i('start split_by_manifest_test.')
    shutil.rmtree(output_location, ignore_errors=True)
    split_start = 0
    split_length = 30
    video_split.split_by_manifest(
        filename, split_start, split_length, output_location, output_name)
    assert os.path.exists(ouput) == True
    shutil.rmtree(ouput, ignore_errors=True)
    shutil.rmtree(output_location, ignore_errors=True)
