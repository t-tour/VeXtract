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

import subprocess
from pathlib import Path
from typing import List
import re
import tempfile
import shutil

from crawler.interface import Crawler
from crawler.DTO import *


class TwitchCrawler(Crawler):

    CRAWLER_REPOSITORY_PATH = Path(_ROOT, "file", "crawler", "tiwitch")
    CLIENT_ID = "miwy5zk23vh2he94san0bzj5ks1r0p"

    def __init__(self, url: str):
        os.makedirs(
            TwitchCrawler.CRAWLER_REPOSITORY_PATH.as_posix(), exist_ok=True)
        self.url = url
        self.vid: str = None
        matched = re.match(r"https?://www\.twitch\.tv/videos/(\d+)\?.*", url)
        subprocess.run(
            ["tcd", "--client-id", "miwy5zk23vh2he94san0bzj5ks1r0p"], capture_output=True)
        if not matched:
            raise Exception(f"twitch 輸入網址錯誤  url={url}")
        else:
            self.vid = matched.group(1)

    def info_crawler(self) -> CrawlableInfo:
        # TODO: Implement Request.
        raise NotImplementedError

    def file_crawler(self) -> Path:
        p = subprocess.Popen(["twitch-dl", 'download', "--no-color",
                              self.vid], stdin=subprocess.PIPE, encoding='utf-8')
        p.stdin.write('4\n')
        p.stdin.flush()
        p.wait()
        for workdirfile in os.listdir(_ROOT):
            matched = re.match(r'\d+_' + self.vid + r'_.+\.mkv', workdirfile)
            if matched:
                shutil.move(os.path.join(_ROOT, matched.group(0)),
                           os.path.join(TwitchCrawler.CRAWLER_REPOSITORY_PATH, matched.group(0)))
                return Path(os.path.join(TwitchCrawler.CRAWLER_REPOSITORY_PATH, matched.group(0)))

    def real_time_comments_crawler(self) -> List[RealTimeComment]:
        realtimecomments = []
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                ["tcd", "-v", self.vid, '-o', tmp],
                capture_output=True
            )
            with open(os.path.join(tmp, self.vid + ".txt"), encoding='utf-8') as reader:
                textlines = reader.read().splitlines()
                for text in textlines:
                    matched = re.match(
                        r'\[(\d+):(\d+):(\d+)\] <(.+)> (.*)', text)
                    if matched:
                        timeat = (
                            int(matched.group(1)) * 3600 * 1000 +
                            int(matched.group(2)) * 60 * 1000 +
                            int(matched.group(3)) * 1000)
                        id_ = matched.group(4)
                        text = matched.group(5)
                        realtimecomments.append(
                            RealTimeComment(timeat, text, id_))
        return realtimecomments

    def comments_crawler(self) -> List[Comment]:
        # TODO: Implement Request.
        raise NotImplementedError

    def clean_info(self):
        # TODO: Implement Request.
        raise NotImplementedError

    def clean_video(self):
        # TODO: Implement Request.
        raise NotImplementedError
