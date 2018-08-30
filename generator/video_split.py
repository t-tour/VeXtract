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
import subprocess
import re
import math
import json
from optparse import OptionParser


def split_by_manifest(filename, split_start, split_length, rename_to, cmd_extra_code="", vcodec="copy", acodec="copy",
                      extra="", **kwargs):
    split_cmd = "ffmpeg -i %s -vcodec %s -acodec %s -y %s" % (filename,
                                                              vcodec,
                                                              acodec,
                                                              extra)
    split_str = " -ss " + str(split_start) + " -t " + \
        str(split_length) + " " + rename_to
    log.i("########################################################")
    log.i("About to run: "+cmd_extra_code + split_cmd+split_str)
    log.i("########################################################")
    subprocess.Popen(cmd_extra_code + split_cmd+split_str,
                     shell=True, stdout=subprocess.PIPE).stdout.read()


def split_by_files(filename, manifest, vcodec="copy", acodec="copy",
                   extra="", **kwargs):
    """ Split video into segments based on the given manifest file.
    Arguments:
        filename (str)      - Location of the video.
        manifest (str)      - Location of the manifest file.
        vcodec (str)        - Controls the video codec for the ffmpeg video
                            output.
        acodec (str)        - Controls the audio codec for the ffmpeg video
                            output.
        extra (str)         - Extra options for ffmpeg.
    """
    if not os.path.exists(manifest):
        log.i("File does not exist: "+manifest)
        raise SystemExit

    with open(manifest) as manifest_file:
        manifest_type = manifest.split(".")[-1]
        if manifest_type == "json":
            config = json.load(manifest_file)
        elif manifest_type == "csv":
            config = csv.DictReader(manifest_file)
        else:
            log.i("Format not supported. File must be a csv or json file")
            raise SystemExit

        split_cmd = "ffmpeg -i %s -vcodec %s -acodec %s -y %s" % (filename,
                                                                  vcodec,
                                                                  acodec,
                                                                  extra)
        #split_count = 1
        #split_error = []
        try:
            fileext = filename.split(".")[-1]
        except IndexError as e:
            raise IndexError("No . in filename. Error: ", str(e))
        for video_config in config:
            split_str = ""
            try:
                split_start = video_config["start_time"]
                split_length = video_config.get("end_time", None)
                if not split_length:
                    split_length = video_config["length"]
                filebase = video_config["rename_to"]
                if fileext in filebase:
                    filebase = ".".join(filebase.split(".")[:-1])

                split_str += " -ss " + str(split_start) + " -t " + \
                    str(split_length) + " " + \
                    filebase + "." + fileext
                log.i("########################################################")
                log.i("About to run: "+split_cmd+split_str)
                log.i("########################################################")
                subprocess.Popen(split_cmd+split_str,
                                 shell=True, stdout=subprocess.PIPE).stdout.read()
            except KeyError as e:
                log.i("############# Incorrect format ##############")
                if manifest_type == "json":
                    log.i("The format of each json array should be:")
                    log.i("{start_time: <int>, length: <int>, rename_to: <string>}")
                elif manifest_type == "csv":
                    log.i("start_time,length,rename_to should be the first line ")
                    log.i("in the csv file.")
                log.i("#############################################")
                log.i(e)
                raise SystemExit


def split_by_seconds(filename, split_length, vcodec="copy", acodec="copy",
                     extra="", **kwargs):
    if split_length and split_length <= 0:
        log.i("Split length can't be 0")
        raise SystemExit

    ouput = subprocess.Popen("ffmpeg -i "+filename, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    _, stderr = ouput.communicate()
    stderr = str(stderr)
    start = stderr.index("Duration")
    time = stderr[start+10:start+18].split(":")
    video_length = int(time[0])*3600 + int(time[1])*60 + int(time[2])
    log.i("影片長度為："+video_length+"秒")
    split_count = int(math.ceil(video_length/float(split_length)))
    if(split_count == 1):
        log.i("Video length is less then the target split length.")
        raise SystemExit

    split_cmd = "ffmpeg -i %s -vcodec %s -acodec %s %s" % (filename, vcodec,
                                                           acodec, extra)
    try:
        filebase = ".".join(filename.split(".")[:-1])
        fileext = filename.split(".")[-1]
    except IndexError as e:
        raise IndexError("No . in filename. Error: " + str(e))
    for n in range(0, split_count):
        split_str = ""
        if n == 0:
            split_start = 0
        else:
            split_start = split_length * n

        split_str += " -ss "+str(split_start)+" -t "+str(split_length) + \
            " " + filebase + "-" + str(n) + "." + fileext
        log.i("About to run: "+split_cmd+split_str)
        subprocess.Popen(
            split_cmd+split_str, shell=True, stdout=subprocess.PIPE).stdout.read()


def split_by_chunks(filename, split_count, vcodec="copy", acodec="copy",
                    extra="", **kwargs):
    if split_count and split_count <= 1:
        log.i("Split counts can't be 1 or less")
        raise SystemExit

    ouput = subprocess.Popen("ffmpeg -i "+filename, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    _, stderr = ouput.communicate()
    stderr = str(stderr)
    start = stderr.index("Duration")
    time = stderr[start+10:start+18].split(":")
    video_length = int(time[0])*3600 + int(time[1])*60 + int(time[2])
    log.i("影片長度為："+video_length+"秒")

    split_length = int(math.ceil(video_length/float(split_count)))
    split_cmd = "ffmpeg -i %s -vcodec %s -acodec %s %s" % (filename, vcodec,
                                                           acodec, extra)
    try:
        filebase = ".".join(filename.split(".")[:-1])
        fileext = filename.split(".")[-1]
    except IndexError as e:
        raise IndexError("No . in filename. Error: " + str(e))
    for n in range(0, split_count):
        split_str = ""
        if n == 0:
            split_start = 0
        else:
            split_start = split_length * n

        split_str += " -ss "+str(split_start)+" -t "+str(split_length) + \
            " " + filebase + "-" + str(n) + "." + fileext
        log.i("About to run: "+split_cmd+split_str)
        subprocess.Popen(
            split_cmd+split_str, shell=True, stdout=subprocess.PIPE).stdout.read()


if __name__ == '__main__':
    mode = 0
    filename = input("請輸入檔案名稱：")
    mode = int(input(
        "請輸入要怎麼分割 1.用秒數分割 2.用份數分割 3.自定義檔案分割（json,csv） 4.自定義分割（輸入start_time,length）："))
    if mode == 1:
        split_length = int(input("請輸入每份的秒數："))
        split_by_seconds(filename, split_length)
    elif mode == 2:
        split_count = int(input("請輸入要分割幾份："))
        split_by_chunks(filename, split_count)
    elif mode == 3:
        split_file = input("請輸入自定義的檔案名稱：")
        split_by_files(filename, split_file)
    elif mode == 4:
        split_start = int(input("請輸入開始時間："))
        split_length = int(input("請輸入時間長度："))
        rename_to = input("請輸入分割影片命名：")
        split_by_manifest(filename, split_start, split_length, rename_to)
    else:
        log.i("輸入錯誤")
