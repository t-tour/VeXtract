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

from generator.video import video_contact

output_location = os.path.join(__root, "test\\test_file\\test_temp")
output_name = "test_video_666.mp4"
ouput = os.path.join(output_location, output_name)


def test_contact_by_type():
    log.i('start contact_by_type_test.')
    shutil.rmtree(ouput, ignore_errors=True)
    cmd_extra_code = "cd %s &" % (
        os.path.join(__root, "test\\test_file\\test_video_temp"))
    #cmd_extra_code = "cd %s &" % (os.path.join(output_location, "temp"))
    video_contact.contact_by_type(
        "mp4", output_location, output_name, cmd_extra_code)
    assert os.path.exists(ouput) == True
    shutil.rmtree(ouput, ignore_errors=True)
    shutil.rmtree(output_location, ignore_errors=True)


def test_contact_by_manifest():
    log.i('start contact_by_manifest_test.')
    shutil.rmtree(ouput, ignore_errors=True)
    video_tuple = (os.path.join(
        __root, "test\\test_file\\test_video_temp", "test_video-0.mp4"),
        os.path.join(
        __root, "test\\test_file\\test_video_temp", "test_video-1.mp4"),
        os.path.join(
        __root, "test\\test_file\\test_video_temp", "test_video-2.mp4"),
        os.path.join(
        __root, "test\\test_file\\test_video_temp", "test_video-3.mp4"))
    """
    video_tuple = (os.path.join(__root, "file", "temp", "03-0.mp4"),
                   os.path.join(__root, "file", "temp", "03-1.mp4"),
                   os.path.join(__root, "file", "temp", "03-2.mp4"))
    """
    video_contact.contact_by_manifest(
        video_tuple, output_location, output_name)
    assert os.path.exists(ouput) == True
    shutil.rmtree(ouput, ignore_errors=True)
    shutil.rmtree(output_location, ignore_errors=True)