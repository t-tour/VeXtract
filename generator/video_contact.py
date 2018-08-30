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
import subprocess
import re
import math
from optparse import OptionParser


def contact_by_type(video_type, output_type, cmd_extra_code=""):
    contact_cmd = "(for %i in (*." + video_type + \
        ") do @echo file '%i') > mylist.txt"
    log.i("########################################################")
    log.i("About to run: "+cmd_extra_code + contact_cmd)
    log.i("########################################################")
    subprocess.Popen(cmd_extra_code+contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    contact_cmd = "ffmpeg -f concat -i mylist.txt -c copy output."+output_type
    log.i("########################################################")
    log.i("About to run: "+cmd_extra_code + contact_cmd)
    log.i("########################################################")
    subprocess.Popen(cmd_extra_code+contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    subprocess.Popen("move output.mp4 "+os.path.join(__root, "file"), shell=True,
                     stdout=subprocess.PIPE).stdout.read()


def contact_by_manifest(output_type):
    contact_cmd = "ffmpeg -f concat -i mylist.txt -c copy output."+output_type
    log.i("########################################################")
    log.i("About to run: "+contact_cmd)
    log.i("########################################################")
    subprocess.Popen(contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    subprocess.Popen("move output.mp4 "+os.path.join(__root, "file"), shell=True,
                     stdout=subprocess.PIPE).stdout.read()


if __name__ == '__main__':
    video_type = input("請輸入要合併的影片類型：")
    output_type = input("請輸入要輸出的影片類型：")
    contact_by_type(video_type, output_type)
