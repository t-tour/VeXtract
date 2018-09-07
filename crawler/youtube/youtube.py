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

import json

from crawler.youtube import youtube_info
from crawler.youtube import youtube_video
from crawler.youtube import youtube_comment

DESTENATION = __root + os.sep.join(['file', 'crawler', 'youtube'])


def info_crawler(url):
    video_info = youtube_info.get_video_by_url(url)
    return video_info


def file_crawler(url, des=DESTENATION):
    video_id = youtube_info.get_video_by_url(url).videoid
    des = des + os.sep + video_id
    if not os.path.exists(des):
        os.makedirs(des)
    log.i('download:', video_id, 'to', des)
    status = youtube_video.download_video(url, des)
    log.i('download:', video_id, 'finished')
    return status


def comment_crawler(url, des=DESTENATION):
    video_id = youtube_info.get_video_by_url(url).videoid
    video_comments = youtube_comment.download_comments(video_id)
    with open(DESTENATION + os.sep + video_id + '.json', 'w', encoding='utf-8') as fp:
        for comment in video_comments:
            fp.write(json.dumps(comment))
    return True


def real_time_comment_crawler(url):
    # TODO: 記得要寫及時留言爬蟲
    pass
