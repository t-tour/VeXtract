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

from generator import video_contact
from generator import video_split
import subprocess
import re
import math
from optparse import OptionParser


def video_process(filename, split_list):
    count = 0
    video_name = filename.split(".")[0]
    video_type = filename.split(".")[1]
    subprocess.Popen("md temp", shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    for i in split_list:
        split_start = float(i[0])
        split_length = float(i[1])-split_start
        rename_to = video_name + "-"+str(count)+"."+video_type
        count = count+1
        video_split.split_by_manifest(os.path.join(os.getcwd(
        ), filename), split_start, split_length, rename_to, cmd_extra_code="cd temp &")

    video_contact.contact_by_type(
        video_type, video_type, cmd_extra_code="cd temp &")
    subprocess.Popen("cd temp & move output.mp4 "+os.path.join(__root,"file"), shell=True,
                     stdout=subprocess.PIPE).stdout.read()


if __name__ == "__main__":
    # 測試用

    # 傳入的list of tuple
    # split_list=[(5,15),(20,35),(50,70)]
    split_list = [(5, 6), (7, 8), (9, 10)]

    video_process("03.mp4", split_list)  # (檔案名稱,list of tuple)
