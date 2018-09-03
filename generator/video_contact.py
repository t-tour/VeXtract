import subprocess
import re
import math
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

from optparse import OptionParser


def contact_by_type(video_type, output_type, output_name="output", cmd_extra_code=""):
    contact_cmd = "(for %i in (*." + video_type + \
        ") do @echo file '%i') > mylist.txt"
    log.i("########################################################")
    log.i("About to run: "+cmd_extra_code + contact_cmd)
    log.i("########################################################")
    subprocess.Popen(cmd_extra_code+contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    contact_cmd = "ffmpeg -f concat -i mylist.txt -c copy "+output_name+"."+output_type
    log.i("########################################################")
    log.i("About to run: "+cmd_extra_code + contact_cmd)
    log.i("########################################################")
    subprocess.Popen(cmd_extra_code+contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    subprocess.Popen(cmd_extra_code + "del mylist.txt &move "+output_name+"."+output_type+" "+os.path.join(__root, "file"), shell=True,
                     stdout=subprocess.PIPE).stdout.read()


def contact_by_manifest(video_tuple, output_type, output_name="output"):
    for i in video_tuple:
        contact_cmd = "echo file '{0}'>>mylist.txt".format(i)
        subprocess.Popen(contact_cmd, shell=True,
                         stdout=subprocess.PIPE).stdout.read()
    contact_cmd = "ffmpeg -f concat -safe 0 -i mylist.txt -c copy " + \
        output_name+"."+output_type
    log.i("########################################################")
    log.i("About to run: "+contact_cmd)
    log.i("########################################################")
    subprocess.Popen(contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    subprocess.Popen("del mylist.txt &move "+output_name+"."+output_type+" " +
                     os.path.join(__root, "file"), shell=True, stdout=subprocess.PIPE).stdout.read()


if __name__ == '__main__':
    # 測試用
    video_tuple = ("03-0.mp4",
                   "03-1.mp4", "03-2.mp4")
    contact_by_manifest(video_tuple, "mp4")
