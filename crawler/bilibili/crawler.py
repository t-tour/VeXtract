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
from pathlib import Path
from urllib import parse
import re
import json


from bs4 import BeautifulSoup
import requests


from crawler.interface import Crawler
from crawler.DTO import CrawlableInfo, RealTimeComment, Comment
from crawler.bilibili.bilibiliDTO import BilibiliComment, BilibiliCrawlableInfo, BilibiliRealTimeComment

HEADER = {
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/67.0.3396.99 Safari/537.36"),
    "Referer": "https://www.bilibili.com",
    "origin": "https://www.bilibili.com"
}


class BilibiliCrawler(Crawler):

    @log.logit
    def __init__(self, url):
        super().__init__(url)
        self._url_normalize()
        self.CRAWLER_REPOSITORY_PATH = Path(
            self.CRAWLER_REPOSITORY_PATH, "bilibili", self.avnumber)
        self.save_crawlable_info_PATH = Path(
            self.CRAWLER_REPOSITORY_PATH, self.avnumber + ".json")

        if self.save_crawlable_info_PATH.exists():
            with self.save_crawlable_info_PATH.open(encoding='utf-8') as f:
                jsonobj = json.load(f)
                for key, value in jsonobj.items():
                    if re.search("PATH", key):
                        self.__setattr__(key, Path(value))
                    else:
                        self.__setattr__(key, value)
        else:
            self._fetch_bilibili()
        print()

    def _html2json(self, html):
        bf = BeautifulSoup(html, 'html.parser')
        scripts_tag = bf.find_all("script")
        start_initial = re.escape("window.__INITIAL_STATE__=")
        end_initial = re.escape(
            ";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1])" +
            ".parentNode.removeChild(s);}());")
        start_play = re.escape("window.__playinfo__=")
        for tag in scripts_tag:
            match_initial = re.match(
                start_initial + "(.+)" + end_initial, str(tag.string))
            match_playinfo = re.match(start_play + "(.+)", str(tag.string))
            if match_initial:
                self.html_initial_json = json.loads(match_initial.group(1))
            if match_playinfo:
                self.html_playinfo_json = json.loads(match_playinfo.group(1))
        if self.html_initial_json["aid"] == None:
            error_message = "Html parse initial_JSON failed.  Check server."
            log.e(error_message)
            raise Exception(error_message)
        if len(self.html_playinfo_json["data"]["durl"]) == 0:
            error_message = "download url is None.  Check server."
            log.e(error_message)
            raise Exception(error_message)

    @log.logit
    def _fetch_bilibili(self):
        req = requests.get(self.url, headers=HEADER)
        self._html2json(req.text)
        os.makedirs(
            self.save_crawlable_info_PATH.parent.as_posix(), exist_ok=True)
        with self.save_crawlable_info_PATH.open(mode='w', encoding='utf-8') as f:
            print(type(f))
            json.dump(self, f, default=self._json_dump_default,
                      ensure_ascii=False)
        # print()

        # log.i('request {} finish.'.format(req.url))
        # bf = BeautifulSoup(req.text, 'html.parser')
        # scripts_tag = bf.find_all("script")
        # start_initial = re.escape("window.__INITIAL_STATE__=")
        # end_initial = re.escape(
        #     ";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1])" +
        #     ".parentNode.removeChild(s);}());")
        # start_play = re.escape("window.__playinfo__=")
        # as_av_info = Bilibili_file_info()
        # for tag in scripts_tag:
        #     re_initial = re.match(start_initial + "(.+)" +
        #                           end_initial, str(tag.string))
        #     re_playinfo = re.match(start_play + "(.+)", str(tag.string))
        #     m = re_initial if re_initial is not None else re_playinfo
        #     if m is not None and m is re_initial:
        #         log.i('__initial_state__ json detected.')
        #         results = json.loads(m.group(1))
        #         if len(results["error"]) is 0:
        #             as_av_info.aid = results["aid"]
        #             for cid in results["videoData"]["pages"]:
        #                 as_av_info.cid.append(str(cid["cid"]))
        #                 as_av_info.cid_name.append(cid["part"])
        #             for tag in results["tags"]:
        #                 as_av_info.video_tags.append(tag["tag_name"])
        #             as_av_info.video_title = results["videoData"]["title"]
        #             as_av_info.video_desc = results["videoData"]["desc"]
        #             as_av_info.video_pubdate = results["videoData"]["pubdate"]
        #             as_av_info.video_pic = results["videoData"]["pic"]
        #         else:
        #             log.e('__initial_state__ error: {}'.format(
        #                 results["error"]))
        #             raise Exception(results["error"])
        #     elif m is not None and m is re_playinfo:
        #         log.i('__playinfo__ json detected.')
        #         results = json.loads(m.group(1))
        #         for url in results["data"]["durl"]:
        #             as_av_info.durl.append(url["url"])
        #         as_av_info.timelength = results["data"]["timelength"]
        #         as_av_info.accept_format = results["data"]["accept_format"]
        #         as_av_info.accept_quality = results["data"]["accept_quality"]
        #         as_av_info.accept_description = results["data"]["accept_description"]
        # comments_dict = dict()
        # log.i('start download comments.')
        # for cid in as_av_info.cid:
        #     comments_dict.update({cid: _cid_comments_list(cid)})
        #     as_av_info.comments = comments_dict
        # if as_av_info.aid is None:
        #     log.e('target object aid is None.  initial state parse failed.')
        #     raise Exception(
        #         "Html parse JSON failed.  INITIAL state can't parse!!  please check {} is correct".format(req.url))
        # if len(as_av_info.durl) == 0:
        #     log.e('target object durl is None.  playinfo parse failed.  please check {} is correct'.format(
        #         req.url))
        #     raise Exception("Html parse JSON failed.  playinfo can't parse!!")
        # log.i('fetch bilibili finish.')
        # return as_av_info

    def _url_normalize(self):
        url_parsed = parse.urlsplit(self.url)
        match_host = re.match(r"^www.bilibili.com$", url_parsed.hostname)
        match_path = re.match(r"^/video/(av[0-9]+)/?$", url_parsed.path)
        match_query = re.search(r"p=(\d+)", url_parsed.query)
        self.avnumber = match_path.group(1)

        if match_host and match_path:
            self.url = f"https://{url_parsed.hostname}{url_parsed.path}"
            if match_query:
                self.url += match_query.group(0)
                self.p = match_query.group(1)
            else:
                self.url += "/?p=1"
                self.p = 1
        else:
            log.e('輸入格式錯誤OAO')
            raise Exception("輸入格式錯誤OAO")

    def info_crawler(self) -> CrawlableInfo:
        length = self.html_playinfo_json["data"]["timelength"]
        pubdate_UTC = self.html_initial_json["videoData"]["pubdate"]
        thumbnail_url = self.html_initial_json["videoData"]["pic"]
        tags = [tag["tag_name"] for tag in self.html_initial_json["tags"]]
        aid = self.html_initial_json["aid"]
        cid = self.html_initial_json["videoData"]["pages"][self.p - 1]["cid"]
        cid_name = self.html_initial_json["videoData"]["pages"][self.p - 1]["part"]
        title = self.html_initial_json["videoData"]["title"]
        uploader = self.html_initial_json['videoData']['owner']['name']
        # TODO: 有時間需要再去找views
        views = 0
        description = self.html_initial_json["videoData"]["desc"]
        Bilibili_crawlable_info = BilibiliCrawlableInfo(
            aid, cid, cid_name, length, title, description, pubdate_UTC, thumbnail_url, tags, uploader, views)
        return Bilibili_crawlable_info

    def file_crawler(self) -> Path:
        crawlable_info = self.info_crawler()
        file_save_path = Path(self.CRAWLER_REPOSITORY_PATH,
                              crawlable_info.videoname + ".flv")
        if file_save_path.exists():
            return file_save_path
        else:
            header = HEADER.copy()
            header.update(
                {"Referer": "https://www.bilibili.com/video/{0}/?p={1}".format(self.avnumber, self.p)})
        # TODO: 接續這個

    def real_time_comments_crawler(self) -> List[RealTimeComment]:
        # TODO: Implement Request.
        raise NotImplementedError

    def comments_crawler(self) -> List[Comment]:
        # TODO: Implement Request.
        raise NotImplementedError

    def clean_info(self):
        # TODO: Implement Request.
        raise NotImplementedError
        return super().clean_info()

    def clean_video(self):
        # TODO: Implement Request.
        raise NotImplementedError
        return super().clean_video()
