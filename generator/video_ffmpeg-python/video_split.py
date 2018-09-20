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
import datetime
import shutil
import subprocess
import re
import math
import json
from optparse import OptionParser

import ffmpeg

from analyzer.algorithm import video_algorithm


def split_by_frame(filename, start_time, frame_number, output_location="", ifMain=True):
    """
    從影片的特定時間點切出一張一張的frame
    filename: 影片路徑
    start_time: 切割開始的時間點
    frame_number: 要切的frame張數
    output_location: 輸出位置(不包含檔案)，預設為__root/file/generator 
    frames的輸出: 會在output_location產生一個[filename的檔案名稱]+_frames的資料夾，並存放切出的frames，
                  如果有存在相同資料夾，則會自動在後面加上_1,_2,...
    ifMain: 控制log要不要顯示Strat,End
    """
    if ifMain:
        log.i("--------------- Start split_by_frame() --------------- ")
    if output_location == "":
        output_location = os.path.join(__root, "file", "generator")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    if filename.find(os.sep) != -1:
        video_name = os.path.basename(filename)
        video_name = video_name.split(".")[0]
    else:
        video_name = filename.split(".")[0]
        filename = os.path.join(os.getcwd(), filename)
    temp_name = video_name+"_frames"
    ouput_temp = os.path.join(output_location, temp_name)
    check = False
    i = 0
    while not check:
        i = i+1
        if os.path.exists(ouput_temp):
            check = False
            temp_name = video_name+"_frames_"+str(i)
            ouput_temp = os.path.join(output_location, temp_name)
        else:
            check = True
    os.makedirs(ouput_temp, exist_ok=True)
    video_fps = video_algorithm.get_video_fps(filename)
    output = os.path.join(ouput_temp, video_name)
    split_cmd = "ffmpeg -i \"%s\" -ss %s -r %s -vframes %s -y \"%s-%s.jpg\"" % (
        filename, str(start_time), str(video_fps), str(frame_number), output, "%d")
    log.i("About to run: " + split_cmd)
    (
        ffmpeg
        .input(filename)
        .output(output+"-%d.jpg", ss=start_time, r=video_fps, vframes=frame_number)
        .run()
    )
    if ifMain:
        log.i("--------------- End split_by_frame() --------------- ")


def split_by_manifest(filename, split_start, split_length, output_location="", output_name="", bitrate="5000k", ifMain=True):
    """
    依照自訂義時間切割影片
    filename: 影片路徑
    split_start: 切割開始的時間點
    split_length: 要切割的時間長度
    output_location: 輸出位置(不包含檔案)，預設為__root/file/generator
    output_name: output_name: [影片名稱].[副檔名]，預設為[filename的檔名]+_output_+時戳，副檔名則參照輸入檔案
    bitrate: 影片位元速率，越大畫質越好，檔案容量也越大，預設為5000k
    ifMain: 控制log要不要顯示Strat,End
    """
    if ifMain:
        log.i("--------------- Start split_by_manifest() --------------- ")
    if output_location == "":
        output_location = os.path.join(__root, "file", "generator")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    defalut_ext = os.path.basename(filename).split(".")[-1]
    video_name = os.path.basename(filename).split(".")[0]
    if output_name == "":
        output_name = video_name+"_output_" + \
            datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    if output_name.split(".")[-1] == output_name:
        output_name = output_name+"."+defalut_ext
    output = os.path.join(output_location, output_name)
    if int(split_start) < 0.1:
        split_start = 0.1
    if int(split_length) < 1:
        split_length = 1
    split_cmd = "ffmpeg -i \"%s\" -ss %s -t %s -avoid_negative_ts make_zero -b:v %s -threads 4 -y \"%s\"" % (
        filename, str(split_start), str(split_length), bitrate, output)
    log.i("About to run: " + split_cmd)
    (
        ffmpeg
        .input(filename)
        .output(output, ss=split_start, t=split_length,
                avoid_negative_ts="make_zero", threads=4, **{"b:v": bitrate})
        .run()
    )
    if ifMain:
        log.i("--------------- End split_by_manifest() --------------- ")


if __name__ == '__main__':
    # 測試用
    filename = os.path.join(__root, "file", "03 666 444.mp4")
    #split_by_frame(filename, 38, 48)
    split_start = 0
    split_length = 5
    split_by_manifest(filename, split_start, split_length)
