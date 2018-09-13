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
import subprocess
from optparse import OptionParser

from generator.video import video_contact
from generator.video import video_split
from analyzer.algorithm import video_algorithm


def video_process(filename, split_list, temp_Keep=False, output_location="", output_name="output"):
    """
    影片的裁切與合併
    filename: 影片路徑
    split_list:[(str_time, end_time), ()...]
    output_location: 輸出位置(不包含檔案)
    output_name: 檔名，副檔名參照輸入檔案
    """
    log.i("--------------- Start video_process() --------------- ")
    ifpath = False
    if filename.find(os.sep) != -1:
        ifpath = True
        filepath = filename
        filename = os.path.basename(filepath)

    count = 0
    video_name = filename.split(".")[0]
    video_type = filename.split(".")[-1]
    if video_type == "flv":
        vcodec = "flv"
    else:
        vcodec = "copy"
    os.makedirs("temp", exist_ok=True)
    for i in split_list:
        split_start = float(i[0])
        split_length = float(i[1]) - split_start
        rename_to = video_name+"-"+str(count)+"."+video_type
        count = count + 1
        if ifpath:
            video_split.split_by_manifest(
                filepath, split_start, split_length, rename_to, cmd_extra_code="cd temp &", ifmove=False, vcodec=vcodec)
        else:
            video_split.split_by_manifest(os.path.join(os.getcwd(
            ), filename), split_start, split_length, rename_to, cmd_extra_code="cd temp &", ifmove=False, vcodec=vcodec)
    if output_location == "":
        output_location = os.path.join(__root, "file")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    video_contact.contact_by_type(
        video_type, output_location=output_location, output_name=output_name, cmd_extra_code="cd temp &")
    if temp_Keep == False:
        shutil.rmtree("temp", ignore_errors=True)
    else:
        if os.path.samefile(output_location, os.getcwd()) == False:
            shutil.rmtree(os.path.join(output_location, "temp"),
                          ignore_errors=True)
            log.i("About to run: " + "move temp" + " \""+output_location+"\"")
            subprocess.Popen("move temp" +
                             " \""+output_location + "\"", shell=True, stdout=subprocess.PIPE).stdout.read()
    log.i("--------------- End video_process() --------------- ")


def video_encoding(filename, output_location="", output_name="output.mp4"):
    log.i("--------------- Start video_encoding() --------------- ")
    if output_location == "":
        output_location = os.path.join(__root, "file")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    defalut_ext = os.path.basename(filename).split(".")[-1]
    if output_name.split(".")[0] == output_name:
        output_name = output_name+".mp4"
    prefer_ext = output_name.split(".")[-1]
    encoding_cmd = "ffmpeg -i \"%s\" -f %s \"%s\"" % (
        filename, prefer_ext, output_name)
    log.i("About to run: " + encoding_cmd)
    subprocess.Popen(encoding_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    log.i("About to run: " + "move " +
          "\"" + output_name+"\"" + " \""+output_location+"\"")
    subprocess.Popen("move "+"\""+output_name+"\"" + " \""+output_location+"\"", shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    log.i('input format is {}  and your output format is {}'.format(
        defalut_ext, prefer_ext))
    log.i("--------------- End video_encoding() --------------- ")


if __name__ == "__main__":
    # 傳入的list of tuple
    split_list = [(5, 33.5)]
    #split_list = [(5, 6), (7, 8), (9, 10)]
    filename = os.path.join(__root, "file/output.mp4")
    video_process(filename, split_list,
                  temp_Keep=False)  # (檔案名稱/檔案路徑,list of tuple)
