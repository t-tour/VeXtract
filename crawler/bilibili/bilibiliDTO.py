import os
import sys
__root = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + (os.sep + '..') * (
        len(os.path.dirname(os.path.abspath(__file__)).split(os.sep))
        - os.path.dirname(os.path.abspath(__file__)).split(os.sep).index(
            'VeXtract'
        ) - 1
    )) + os.sep
sys.path.append(__root)
_ROOT = __root

from helper import logger
log = logger.Logger(__name__)

from typing import List

from crawler.DTO import Comment, CrawlableInfo, RealTimeComment


class BilibiliComment(Comment):

    def __init__(self):
        # TODO: Implement Request.
        raise NotImplementedError


class BilibiliCrawlableInfo(CrawlableInfo):

    def __init__(self, aid: int, cid: int, cid_name: str, length_millisecond: int,
                 title: str, description: str, pubdate_UTC: int, thumbnail_url: str, tags: List[str],
                 uploader: str, views: int):
        super().__init__(f'{title}_{cid_name}',
                         f'{aid}_{cid}', uploader, views, description)
        self.length_millisecond = length_millisecond
        self.pubdate_UTC = pubdate_UTC
        self.thumbnail_url = thumbnail_url
        self.tags = tags


class BilibiliRealTimeComment(RealTimeComment):

    def __init__(self, user, timeat, text):
        super().__init__(timeat, text, user)
