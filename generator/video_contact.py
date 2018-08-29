import subprocess
import re
import math
import os
from optparse import OptionParser


def contact_by_type(video_type, output_type, cmd_extra_code=""):
    contact_cmd = "(for %i in (*." + video_type + \
        ") do @echo file '%i') > mylist.txt"
    print("########################################################")
    print("About to run: "+cmd_extra_code + contact_cmd)
    print("########################################################")
    subprocess.Popen(cmd_extra_code+contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    contact_cmd = "ffmpeg -f concat -i mylist.txt -c copy output."+output_type
    print("########################################################")
    print("About to run: "+cmd_extra_code + contact_cmd)
    print("########################################################")
    subprocess.Popen(cmd_extra_code+contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()


def contact_by_manifest(output_type):
    contact_cmd = "ffmpeg -f concat -i mylist.txt -c copy output."+output_type
    print("########################################################")
    print("About to run: "+contact_cmd)
    print("########################################################")
    subprocess.Popen(contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()


if __name__ == '__main__':
    video_type = input("請輸入要合併的影片類型：")
    output_type = input("請輸入要輸出的影片類型：")
    contact_by_type(video_type, output_type)
