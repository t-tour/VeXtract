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


def video_process(filename, split_list, temp_Keep=False, output_location="", output_name="output"):
    log.i("--------------- Start video_process() --------------- ")
    ifpath = False
    if filename.find(os.sep) != -1:
        ifpath = True
        filepath = filename
        filename = os.path.basename(filepath)

    count = 0
    video_name = filename.split(".")[0]
    video_type = filename.split(".")[-1]
    os.makedirs("temp", exist_ok=True)
    for i in split_list:
        split_start = float(i[0])
        split_length = float(i[1]) - split_start
        rename_to = video_name+"-"+str(count)+"."+video_type
        count = count + 1
        if ifpath:
            video_split.split_by_manifest(
                filepath, split_start, split_length, rename_to, cmd_extra_code="cd temp &", ifmove=False)
        else:
            video_split.split_by_manifest(os.path.join(os.getcwd(
            ), filename), split_start, split_length, rename_to, cmd_extra_code="cd temp &", ifmove=False)
    if output_location == "":
        output_location = os.path.join(__root, "file")
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


if __name__ == "__main__":
    # 傳入的list of tuple
    split_list = [(5, 20), (30, 45), (60, 75)]
    #split_list = [(5, 6), (7, 8), (9, 10)]
    filename = os.path.join(__root, "file", "03.mp4")
    video_process(filename, split_list, output_location=os.path.join(__root, "file", "generator"),
                  temp_Keep=True, output_name="03-666.flv")  # (檔案名稱/檔案路徑,list of tuple)
