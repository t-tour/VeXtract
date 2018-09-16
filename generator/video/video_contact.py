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

import random
import subprocess
from optparse import OptionParser


def contact_by_type(video_type, input_location="", output_location="", output_name=""):
    """
    把路徑底下，所有同類型的影片合併
    video_type: 要合併的影片類型
    input_location: 要合併影片的路徑
    output_location: 輸出位置(不包含檔案)，預設為__root/file/generator
    output_name: [影片名稱].[副檔名]，預設為contact_output_[一段五位數Random亂數]]，副檔名則參照video_type
    """
    log.i("--------------- Start contact_by_type() --------------- ")
    if input_location == "":
        input_location = os.getcwd()
    if output_location == "":
        output_location = os.path.join(__root, "file", "generator")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    random_number = "".join(random.sample(
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 5))
    contact_list_name = "contact_list_"+random_number+".txt"
    contact_cmd = "(for %i in (*." + video_type + \
        ") do @echo file '%i') > " + contact_list_name
    contact_cmd = "cd " + "\""+input_location+"\""+" &" + contact_cmd
    log.i("About to run: " + contact_cmd)
    subprocess.Popen(contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    if output_name == "":
        output_name = "contact_ouput_" + random_number
    if output_name.split(".")[-1] == output_name:
        output_name = output_name+"."+video_type
    output = os.path.join(output_location, output_name)
    contact_cmd = "ffmpeg -f concat -i %s -c copy -y \"%s\" &del %s" % (
        contact_list_name, output, contact_list_name)
    contact_cmd = "cd " + "\""+input_location+"\""+" &" + contact_cmd
    log.i("About to run: " + contact_cmd)
    subprocess.Popen(contact_cmd, shell=True,
                     stdout=subprocess.PIPE).stdout.read()
    log.i("--------------- End contact_by_type() --------------- ")


def contact_by_manifest(video_tuple, output_location="", output_name=""):
    """
    依照自訂義的video_tuple，照順序把影片合併
    video_tuple: 要合併的影片集合，tuple格式：(影片1,影片2,...)，影片請輸入絕對路徑，不然則預設為執行目錄底下開始
    output_location: 輸出位置(不包含檔案)，預設為__root/file/generator
    output_name: [影片名稱].[副檔名]，預設為contact_output_[一段五位數Random亂數]]，副檔名則參照video_tuple的第一個檔案
    """
    log.i("--------------- Start contact_by_manifest() --------------- ")
    if output_location == "":
        output_location = os.path.join(__root, "file", "generator")
    if not os.path.exists(output_location):
        os.makedirs(output_location, exist_ok=True)
    random_number = "".join(random.sample(
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 5))
    contact_list_name = "contact_list_"+random_number+".txt"
    video_type = video_tuple[0].split(".")[-1]
    if output_name == "":
        output_name = "contact_ouput_"+random_number
    if output_name.split(".")[-1] == output_name:
        output_name = output_name+"."+video_type
    output = os.path.join(output_location, output_name)
    for i in video_tuple:
        contact_cmd = "echo file '%s'>>%s" % (i, contact_list_name)
        log.i("About to run: " + contact_cmd)
        subprocess.Popen(contact_cmd, shell=True,
                         stdout=subprocess.PIPE).stdout.read()
    contact_cmd = "ffmpeg -f concat -safe 0 -i %s -c copy -y \"%s\" &del %s" % (
        contact_list_name, output, contact_list_name)
    log.i("About to run: " + contact_cmd)
    subprocess.Popen(contact_cmd, shell=True, stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE, stdin=subprocess.PIPE).stdout.read()
    log.i("--------------- End contact_by_manifest() --------------- ")


if __name__ == '__main__':
    # 測試用

    video_tuple = (os.path.join(__root, "file", "temp", "03-0.mp4"),
                   os.path.join(__root, "file", "temp", "03-1.mp4"),
                   os.path.join(__root, "file", "temp", "03-2.mp4"))

    contact_by_manifest(video_tuple)
