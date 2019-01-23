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
_ROOT = __root

from helper import logger
log = logger.Logger(__name__)

# Please use 繼承
class RealTimeComment():

    def __init__(self, timeat, text, id=None):
        self.timeat = timeat
        self.text = text
        self.id = id


class Comment():

    def __init__(self, pubdate, text, id):
        self.pubdate = pubdate
        self.text = text
        self.id = id


class CrawlableInfo():

    def __init__(self, videoname, videoid, uploader, views, description):
        self.videoname = videoname
        self.videoid = videoid
        self.uploader = uploader
        self.views = views
        self.description = description
