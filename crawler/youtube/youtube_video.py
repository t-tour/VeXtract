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

from pytube import YouTube

from crawler.youtube import youtube_info

def download_video(url, des=__root + os.sep.join(['file', 'youtube'])):
    video_id = youtube_info.get_video_by_url(url).videoid
    des = des + os.sep + video_id
    log.i('download:', video_id, 'to', des)
    if not os.path.exists(des):
        os.makedirs(des)
    YouTube(url).streams.first().download(des)
    log.i('download:', video_id, 'finished')
    return True

if __name__ == '__main__':
    status = download_video("https://www.youtube.com/watch?v=bMt47wvK6u0")