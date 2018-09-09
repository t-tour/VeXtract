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

import pafy


def get_video_by_url(url, is_playlist=False, index=0):
    if is_playlist:
        playlist = pafy.get_playlist(url)['items']
        if not(len(playlist) > index and index >= 0):
            index = 0
        video = playlist[index]['pafy']
    else:
        video = pafy.new(url)

    return video


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=bMt47wvK6u0"
    video = get_video_by_url(url)
    print(video.videoid)
    print(video.getbest().url)
