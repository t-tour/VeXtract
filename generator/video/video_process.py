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
import shutil

import ffmpeg

from generator.video import video_split, video_contact
from analyzer.algorithm import video_algorithm


def video_process(filename, split_list, temp_Keep=False, output_location="", output_name="", ifMain=True, ifLog=False, ifStdout=False):
    """
    影片的裁切與合併
    filename: 影片路徑
    split_list:[(start_time1, end_time1), (start_time2,end_time2))...]
    output_location: 輸出位置(不包含檔案)，預設為__root/file/generator
    output_name: [影片名稱].[副檔名]，預設為[filename的檔名]+_output_+時戳，副檔名則參照輸入檔案
    temp_Keep: 處理時會在output_location產生[filename的檔案名稱]+_process_temp的資料夾，
               可選擇是否保留，如果有存在相同資料夾，則會自動在後面加上_1,_2,...
    ifMain: 控制log要不要顯示Strat,End，預設為True
    ifLog: 控制要不要把python-ffmpeg執行過程轉換成ffmpeg的cmd指令顯示在log，複寫ifMain，預設為False
    ifStdout: 控制要不要顯示ffmpeg的stdout訊息，否則只顯示error訊息，預設為False
    """
    if ifMain and ifLog:
        log.i("--------------- Start video_process() --------------- ")
    if output_location == "":
        output_location = os.path.join(__root, "file", "generator")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    ifpath = False
    if filename.find(os.sep) != -1:
        ifpath = True
        filepath = filename
        filename = os.path.basename(filepath)
    count = 0
    video_name = filename.split(".")[0]
    video_type = filename.split(".")[-1]
    if output_name == "":
        output_name = video_name+"_output_" + \
            datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    temp_name = video_name+"_process_temp"
    ouput_temp = os.path.join(output_location, temp_name)
    check = False
    i = 0
    while not check:
        i = i+1
        if os.path.exists(ouput_temp):
            check = False
            temp_name = video_name+"_process_temp_"+str(i)
            ouput_temp = os.path.join(output_location, temp_name)
        else:
            check = True
    os.makedirs(ouput_temp, exist_ok=True)
    split_list_digit = len(str(len(split_list)))
    if ifLog:
        log.i("--------------- Start split_by_manifest() --------------- ")
    for i in split_list:
        split_start = float(i[0])
        split_length = float(i[1]) - split_start
        rename_to = video_name+"-" + \
            str(count).zfill(split_list_digit)+"."+video_type
        count = count + 1
        if ifpath:
            video_split.split_by_manifest(
                filepath, split_start, split_length, output_location=ouput_temp, output_name=rename_to, ifMain=False, ifLog=ifLog, ifStdout=ifStdout)
        else:
            video_split.split_by_manifest(os.path.join(os.getcwd(
            ), filename), split_start, split_length, output_location=ouput_temp, output_name=rename_to, ifMain=False, ifLog=ifLog, ifStdout=ifStdout)
    if ifLog:
        log.i("--------------- End split_by_manifest() --------------- ")
    video_contact.contact_by_type(
        video_type, input_location=ouput_temp, output_location=output_location, output_name=output_name)
    if not temp_Keep:
        shutil.rmtree(ouput_temp, ignore_errors=True)
    if ifMain and ifLog:
        log.i("--------------- End video_process() --------------- ")


def video_encoding(filename, output_location="", output_name="", bitrate="5000k", ifMain=True, ifLog=False, ifStdout=False):
    """
    影片的轉檔，根據ouput_name的副檔名做重新編碼
    filename: 影片路徑
    output_location: 輸出位置(不包含檔案)，預設為__root/file/generator
    output_name: [影片名稱].[副檔名]，預設為[filename的檔名]+_output_+時戳，副檔名則預設為mp4
    bitrate: 影片位元速率，越大畫質越好，檔案容量也越大，預設為5000k
    ifMain: 控制log要不要顯示Strat,End，預設為True
    ifLog: 控制要不要把python-ffmpeg執行過程轉換成ffmpeg的cmd指令顯示在log，複寫ifMain，預設為False
    ifStdout: 控制要不要顯示ffmpeg的stdout訊息，否則只顯示error訊息，預設為False
    """
    if ifMain and ifLog:
        log.i("--------------- Start video_encoding() --------------- ")
    if output_location == "":
        output_location = os.path.join(__root, "file", "generator")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    defalut_ext = os.path.basename(filename).split(".")[-1]
    video_name = os.path.basename(filename).split(".")[0]
    if output_name == "":
        output_name = video_name+"_output_" + \
            datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    if output_name.split(".")[0] == output_name:
        output_name = output_name+".mp4"
    prefer_ext = output_name.split(".")[-1]
    output = os.path.join(output_location, output_name)
    if ifStdout:
        loglevel = "verbose"
    else:
        loglevel = "warning"
    process_cmd = "ffmpeg -i \"%s\" -f %s -b:v %s -threads 4 -loglevel %s -y \"%s\"" % (
        filename, prefer_ext, bitrate, loglevel, output)
    if ifLog:
        log.i("About to run: " + process_cmd)
    (
        ffmpeg
        .input(filename)
        .output(output, f=prefer_ext, threads=4, y="-y", loglevel=loglevel, **{"b:v": bitrate})
        .run()
    )
    log.i('input format is %s  and your output format is %s' %
          (defalut_ext, prefer_ext))
    if ifMain and ifLog:
        log.i("--------------- End video_encoding() --------------- ")


if __name__ == "__main__":
    filename = os.path.join(__root, "test\\test_file", "test_video.mp4")
    output_name = "test_video_666.flv"
    split_list = [(0.0, 4.0), (6.0, 10.0), (13.0, 17.0), (24.0, 28.0)]
    video_process(filename, split_list, temp_Keep=True)
    #video_encoding(filename, output_name=output_name)
