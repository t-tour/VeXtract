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

import datetime
import random
import subprocess
import shutil

import ffmpeg

from optparse import OptionParser


def contact_by_type(video_type, input_location="", output_location="", output_name="", ifMain=True):
    """
    把路徑底下，所有同類型的影片合併
    video_type: 要合併的影片類型
    input_location: 要合併影片的路徑
    output_location: 輸出位置(不包含檔案)，預設為__root/file/generator
    output_name: [影片名稱].[副檔名]，預設為contact_output_+時戳，副檔名則參照video_type
    ifMain: 控制log要不要顯示Strat,End
    """
    if ifMain:
        log.i("--------------- Start contact_by_type() --------------- ")
    if input_location == "":
        input_location = os.getcwd()
    if output_location == "":
        output_location = os.path.join(__root, "file", "generator")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    random_number = "".join(random.sample(
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 5))
    dirs = os.listdir(input_location)
    contact_list = []
    for i in dirs:
        if i.split(".")[-1] == video_type:
            contact_list.append(
                "file " + "'"+os.path.join(input_location, i)+"'" + "\n")
    contact_input = os.path.join(
        output_location, "contact_list_"+random_number+".txt")
    fileopen = open(contact_input, "a")
    fileopen.writelines(contact_list)
    fileopen.close()
    if output_name == "":
        output_name = "contact_output_" + \
            datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    if output_name.split(".")[-1] == output_name:
        output_name = output_name+"."+video_type
    output = os.path.join(output_location, output_name)
    contact_cmd = "ffmpeg -f concat -safe 0 -i \"%s\" -c copy -y \"%s\"" % (
        contact_input, output)
    log.i("About to run: " + contact_cmd)
    (
        ffmpeg
        .input(contact_input, f="concat", safe=0)
        .output(output, c="copy", y="-y")
        .run()
    )
    os.remove(contact_input)
    if ifMain:
        log.i("--------------- End contact_by_type() --------------- ")


def contact_by_manifest(video_tuple, output_location="", output_name="", ifMain=True):
    """
    依照自訂義的video_tuple，照順序把影片合併
    video_tuple: 要合併的影片集合，tuple格式：(影片1,影片2,...)，影片請輸入絕對路徑，不然則預設為執行目錄底下開始
    output_location: 輸出位置(不包含檔案)，預設為__root/file/generator
    output_name: [影片名稱].[副檔名]，預設為contact_output_+時戳，副檔名則參照video_tuple的第一個檔案
    ifMain: 控制log要不要顯示Strat,End
    """
    if ifMain:
        log.i("--------------- Start contact_by_manifest() --------------- ")
    if output_location == "":
        output_location = os.path.join(__root, "file", "generator")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    random_number = "".join(random.sample(
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 5))
    video_type = video_tuple[0].split(".")[-1]
    contact_list = []
    for i in video_tuple:
        contact_list.append("file " + "'"+i+"'" + "\n")
    contact_input = os.path.join(
        output_location, "contact_list_"+random_number+".txt")
    fileopen = open(contact_input, "a")
    fileopen.writelines(contact_list)
    fileopen.close()
    if output_name == "":
        output_name = "contact_output_" + \
            datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    if output_name.split(".")[-1] == output_name:
        output_name = output_name+"."+video_type
    output = os.path.join(output_location, output_name)
    contact_cmd = "ffmpeg -f concat -safe 0 -i \"%s\" -c copy -y \"%s\"" % (
        contact_input, output)
    log.i("About to run: " + contact_cmd)
    (
        ffmpeg
        .input(contact_input, f="concat", safe=0)
        .output(output, c="copy", y="-y")
        .run()
    )
    os.remove(contact_input)
    if ifMain:
        log.i("--------------- End contact_by_manifest() --------------- ")


if __name__ == '__main__':
    # 測試用
    video_tuple = (os.path.join(
        __root, "test\\test_file\\video_test_file", "test_video-0.mp4"),
        os.path.join(
        __root, "test\\test_file\\video_test_file", "test_video-1.mp4"),
        os.path.join(
        __root, "test\\test_file\\video_test_file", "test_video-2.mp4"),
        os.path.join(
        __root, "test\\test_file\\video_test_file", "test_video-3.mp4"))
    input_location = os.path.join(__root, "test\\test_file\\video_test_file")
    contact_by_manifest(video_tuple)
    #contact_by_type("mp4", input_location)
