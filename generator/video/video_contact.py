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
from optparse import OptionParser


def contact_by_type(video_type, output_type, output_name="output", cmd_extra_code=""):
    # FIXME: 以後可能會架在 linux 上面運行 所以需要跨平台的指令
    # FIXME: 沒有修過喔~
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
    subprocess.Popen(cmd_extra_code + "del mylist.txt &move " + output_name + "."+output_type+" \"" + os.path.join(__root, "file")+"\"", shell=True,
                     stdout=subprocess.PIPE).stdout.read()


def contact_by_manifest(video_tuple, output_name="output"):
    # FIXME: 以後可能會架在 linux 上面運行 所以需要跨平台的指令
    defalut_ext = video_tuple[0].split(".").pop()
    prefer_ext = output_name.split(".").pop()
    if output_name == "output":
        output_name = output_name+"."+defalut_ext
    if output_name.find(os.sep) == -1:
        output_name = os.path.join(__root, "file", output_name)
    if prefer_ext != defalut_ext:
        log.i('input format is {}  and your output format is {}'.format(
            defalut_ext, prefer_ext))
    for i in video_tuple:
        contact_cmd = "echo file '{0}'>>mylist.txt".format(i)
        subprocess.Popen(contact_cmd, shell=True,
                         stdout=subprocess.PIPE).stdout.read()
    contact_cmd = "ffmpeg -y -f concat -safe 0 -i mylist.txt -c copy \"{}\"".format(
        output_name)
    log.i("########################################################")
    log.i("About to run: " + contact_cmd)
    log.i("########################################################")
    subprocess.Popen(contact_cmd, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, stdin=subprocess.PIPE).stdout.read()
    subprocess.Popen("del mylist.txt", shell=True,
                     stdout=subprocess.PIPE).stdout.read()


if __name__ == '__main__':
    # 測試用

    video_tuple = ("C:\\Users\\admin10\\Documents\\GitLab\\VeXtract\\temp\\03-0.mp4",
                   "C:\\Users\\admin10\\Documents\\GitLab\\VeXtract\\temp\\03-1.mp4", "C:\\Users\\admin10\\Documents\\GitLab\\VeXtract\\temp\\03-2.mp4")

    contact_by_manifest(video_tuple)