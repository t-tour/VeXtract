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

from analyzer.algorithm import video_algorithm


def split_by_frame(filename, start_time, frame_number):
    if filename[1:2] == ":":
        video_name = os.path.basename(filename)
        video_name = video_name.split(".")[0]
    else:
        video_name = filename.split(".")[0]
        filename = os.path.join(os.getcwd(), filename)
    subprocess.Popen("md temp", shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    video_fps = video_algorithm.get_video_fps(filename)
    split_cmd = "ffmpeg -i %s -ss %s -r %s -vframes %s -y %s-%s.jpg" % (
        filename, str(start_time), str(video_fps), str(frame_number), video_name, "%d")
    log.i("########################################################")
    log.i("About to run: "+"cd temp &" + split_cmd)
    log.i("########################################################")
    subprocess.Popen("cd temp &" + split_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    subprocess.Popen("rd "+os.path.join(__root, "file", "temp")+" /s/q", shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    subprocess.Popen("move temp "+os.path.join(__root, "file"),
                     shell=True, stdout=subprocess.PIPE).stdout.read()


def split_by_manifest(filename, split_start, split_length, rename_to, cmd_extra_code="", ifmove=True, vcodec="copy", acodec="copy",
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
    if ifmove:
        subprocess.Popen(cmd_extra_code + "move "+rename_to+" "+os.path.join(
            __root, "file"), shell=True, stdout=subprocess.PIPE).stdout.read()


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
                subprocess.Popen("move "+filebase + "." + fileext+" "+os.path.join(
                    __root, "file"), shell=True, stdout=subprocess.PIPE).stdout.read()
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

    video_length = video_algorithm.get_video_length(filename)
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
        subprocess.Popen("move "+filebase + "-" + str(n) + "." + fileext+" "+os.path.join(
            __root, "file"), shell=True, stdout=subprocess.PIPE).stdout.read()


def split_by_chunks(filename, split_count, vcodec="copy", acodec="copy",
                    extra="", **kwargs):
    if split_count and split_count <= 1:
        log.i("Split counts can't be 1 or less")
        raise SystemExit

    video_length = video_algorithm.get_video_length(filename)
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
        subprocess.Popen("move "+filebase + "-" + str(n) + "." + fileext+" "+os.path.join(
            __root, "file"), shell=True, stdout=subprocess.PIPE).stdout.read()


if __name__ == '__main__':
    # 測試用
    filename = "F:\Git\VeXtract\generator\\03.mp4"
    split_by_frame(filename, 38, 48)

    #split_by_seconds(filename, split_length)
    #split_by_chunks(filename, split_count)
    #split_by_files(filename, split_file)
    #split_by_manifest(filename, split_start, split_length, rename_to)
