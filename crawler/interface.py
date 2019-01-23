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

from abc import abstractmethod, ABCMeta
from typing import List
from pathlib import Path

from crawler.DTO import RealTimeComment, Comment, CrawlableInfo


class Crawler(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, url: str):
        self.CRAWLER_REPOSITORY_PATH = Path(_ROOT, "file", "crawler")
        self.url = url

    @abstractmethod
    def info_crawler(self) -> CrawlableInfo:
        pass

    @abstractmethod
    def file_crawler(self) -> Path:
        pass

    @abstractmethod
    def real_time_comments_crawler(self) -> List[RealTimeComment]:
        pass

    @abstractmethod
    def comments_crawler(self) -> List[Comment]:
        pass

    @abstractmethod
    def clean_info(self):
        pass

    @abstractmethod
    def clean_video(self):
        pass

    @staticmethod
    def _json_dump_default(o):
        if isinstance(o, Path):
            return o.as_posix()
        else:
            return o.__dict__
