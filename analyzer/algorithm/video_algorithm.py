import subprocess
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


def get_video_length(filename):
    ouput = subprocess.Popen("ffmpeg -i "+filename, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    _, stderr = ouput.communicate()
    stderr = str(stderr)
    start = stderr.index("Duration")
    time = stderr[start+10:start+18].split(":")
    video_length = int(time[0])*3600 + int(time[1])*60 + int(time[2])
    log.i("影片長度為："+video_length+"秒")
    return video_length

def get_video_fps(filename):
    ouput = subprocess.Popen("ffmpeg -i "+filename, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    _, stderr = ouput.communicate()
    stderr = str(stderr)
    start = stderr.index("fps")-4
    video_fps=int(stderr[start:start+3])
    log.i("影片fps為："+str(video_fps))
    return video_fps

if __name__=="__main__":
    #測試用
    filename="F:\Git\VeXtract\generator\\03.mp4"
    get_video_fps(filename)