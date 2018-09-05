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


def get_video_length(filename):
    ouput = subprocess.Popen("ffmpeg -i \"{}\"".format(filename), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    _, stderr = ouput.communicate()
    time = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)",
                     str(stderr, encoding='utf-8'))
    log.i('time length: {}:{}:{}'.format(
        time.group(1), time.group(2), time.group(3)))
    video_length = int(time.group(1))*3600 + \
        int(time.group(2))*60 + float(time.group(3))
    log.i("影片長度為：{:.2f}秒".format(video_length))
    return video_length


def get_video_fps(filename):
    ouput = subprocess.Popen("ffmpeg -i \"{}\"".format(filename), stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    _, stderr = ouput.communicate()
    matcher = re.search(r", ([\d|\.]+) fps", str(stderr, encoding='utf-8'))
    video_fps = float(matcher.group(1))
    log.i("影片fps為：{:.2f}fps".format(video_fps))
    return video_fps


if __name__ == "__main__":
    # 測試用
    get_video_fps(__root + "file\\algorithm\\123.mp4")
