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

from abc import abstractmethod, ABCMeta
from typing import List
from pathlib import Path

from crawler.DTO import RealTimeComment, Comment, CrawlableInfo


class Crawler(metaclass=ABCMeta):

    @abstractmethod
    def info_crawler(self, url) -> CrawlableInfo:
        pass

    @abstractmethod
    def file_crawler(self, url) -> Path:
        pass

    @abstractmethod
    def real_time_comments_crawler(self, url) -> List[RealTimeComment]:
        pass

    @abstractmethod
    def comments_crawler(self, url) -> List[Comment]:
        pass
