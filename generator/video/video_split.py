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

import csv
import shutil
import subprocess
import re
import math
import json
from optparse import OptionParser

from analyzer.algorithm import video_algorithm


def split_by_frame(filename, start_time, frame_number, output_location=""):
    log.i("--------------- Start split_by_frame() --------------- ")
    if filename.find(os.sep) != -1:
        video_name = os.path.basename(filename)
        video_name = video_name.split(".")[0]
    else:
        video_name = filename.split(".")[0]
        filename = os.path.join(os.getcwd(), filename)
    temp_name = video_name+"_temp"
    os.makedirs(temp_name, exist_ok=True)
    video_fps = video_algorithm.get_video_fps(filename)
    split_cmd = "ffmpeg -i \"%s\" -ss %s -r %s -vframes %s -y \"%s-%s.jpg\"" % (
        filename, str(start_time), str(video_fps), str(frame_number), video_name, "%d")
    split_cmd = "cd " + temp_name+" &" + split_cmd
    log.i("About to run: " + split_cmd)
    subprocess.Popen(split_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    if output_location == "":
        output_location = os.path.join(__root, "file", "generator")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    shutil.rmtree(os.path.join(output_location, temp_name), ignore_errors=True)
    split_cmd = "move " + temp_name + " \""+output_location+"\""
    log.i("About to run: " + split_cmd)
    subprocess.Popen(split_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    log.i("--------------- End split_by_frame() --------------- ")


def split_by_manifest(filename, split_start, split_length, output_name="", output_location="", vcodec="copy", acodec="copy",
                      extra="", **kwargs):
    log.i("--------------- Start split_by_manifest() --------------- ")
    if output_location == "":
        output_location = os.path.join(__root, "file", "generator")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    defalut_ext = os.path.basename(filename).split(".")[-1]
    video_name = os.path.basename(filename).split(".")[0]
    if output_name == "":
        output_name = video_name+"_ouput"
    if output_name.split(".")[-1] == output_name:
        output_name = output_name+"."+defalut_ext
    output_name = os.path.join(output_location, output_name)
    output_name = "\""+output_name+"\""
    split_cmd = "ffmpeg -i \"%s\" -vcodec %s -acodec %s -y %s" % (filename,
                                                                  vcodec,
                                                                  acodec,
                                                                  extra)
    split_str = " -ss " + str(split_start) + " -t " + \
        str(split_length) + " " + output_name
    split_cmd = split_cmd + split_str
    log.i("About to run: " + split_cmd)
    subprocess.Popen(split_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    log.i("--------------- End split_by_manifest() --------------- ")


if __name__ == '__main__':
    # 測試用
    filename = os.path.join(__root, "file", "03.mp4")
    split_by_frame(filename, 38, 48)

    #split_by_manifest(filename, split_start, split_length, output_name)
