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
    """
    從影片的特定時間點切出一張一張的frame
    filename: 影片路徑
    start_time: 切割開始的時間點
    frame_number: 要切的frame張數
    output_location: 輸出位置(不包含檔案)，預設為__root/file/generator
    切完之後，會產生一個[filename的檔案名稱]+_temp的資料節，並移到output_location
    """
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
    split_cmd = "move " + "\""+temp_name+"\"" + " \""+output_location+"\""
    log.i("About to run: " + split_cmd)
    subprocess.Popen(split_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    log.i("--------------- End split_by_frame() --------------- ")


def split_by_manifest(filename, split_start, split_length, output_location="", output_name="", bitrate="5000k"):
    """
    依照自訂義時間切割影片
    filename: 影片路徑
    split_start: 切割開始的時間點
    split_length: 要切割的時間長度
    output_location: 輸出位置(不包含檔案)，預設為__root/file/generator
    output_name: output_name: [影片名稱].[副檔名]，預設為[filename的檔名]+_output，副檔名則參照輸入檔案
    bitrate: 影片位元速率，越大畫質越好，檔案容量也越大，預設為5000k
    """
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
    split_cmd = "ffmpeg -ss %s -i \"%s\" -t %s -avoid_negative_ts make_zero -b %s -cpu-used 2 -threads 4 -y \"%s\"" % (
        str(split_start), filename, str(split_length), bitrate, output_name)
    log.i("About to run: " + split_cmd)
    subprocess.Popen(split_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    log.i("--------------- End split_by_manifest() --------------- ")


if __name__ == '__main__':
    # 測試用
    filename = os.path.join(__root, "file", "03.mp4")
    split_by_frame(filename, 38, 48)

    #split_by_manifest(filename, split_start, split_length, output_name)
