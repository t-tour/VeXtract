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
from urllib import parse
import re
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

REALTIME_COMMENT_REQUEST_URL = "https://comment.bilibili.com/"
MAIN_HOST_URL = "https://www.bilibili.com/video/"
COMMENT_REQ_URL = "https://api.bilibili.com/x/v2/reply?jsonp=jsonp&pn={page}&type=1&oid={aid}"
HEADER = {
    "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/67.0.3396.99 Safari/537.36"),
    "Referer": "https://www.bilibili.com",
    "origin": "https://www.bilibili.com"
}


class Bilibili_file_info():
    """
    Attributes:
      aid: AV號數字的部分
      cid: AV號內所有影片的id
      cid_name: 各集的名稱
      timelength: 這集的毫秒數ms
      accept_format: 看看就好
      accept_quality: 看看就好
      accept_quailty_description: 看看就好
      video_title: AV號標題
      video_desc: AV號說明
      video_pubdate: AV號上傳日期
      video_pic: 封面URI
      video_tags: AV號標籤
      durl: 下載位址(需要refer)
      comments: {
          user: 
          sec: 
          text: 
          score: default none
      }
    """
    aid: str
    cid: list
    cid_name: list
    timelength: int
    accept_format: list
    accept_quality: list
    accept_quailty_description: list
    video_title: str
    video_desc: str
    video_pubdate: int
    video_pic: str
    video_tags: list
    durl: list
    comments: dict

    def save(self, path):
        with open(os.path.join(path, 'av{}.json'.format(self.aid)), 'w', encoding='utf-8') as f:
            json.dump(self, f, default=lambda o: o.__dict__,
                      ensure_ascii=False)
        log.i('av{}.json saved'.format(self.aid))

    @staticmethod
    def load(j_data):
        with open(j_data, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            obj = Bilibili_file_info()
            for attr, value in loaded.items():
                obj.__setattr__(attr, value)
        log.i('load {} finish.'.format(j_data))
        return obj

    def __init__(self):
        self.aid = None
        self.cid = list()
        self.cid_name = list()
        self.timelength = 0
        self.accept_format = list()
        self.accept_quality = list()
        self.accept_quailty_description = list()
        self.video_title = None
        self.video_desc = None
        self.video_pubdate = None
        self.video_pic = None
        self.video_tags = list()
        self.durl = list()
        self.comments = dict()

    def __str__(self):
        return str.format(
            "aid:{0}\tvideo_title:{1}\n" +
            "cid:{2}\tcid_title:{3}"
            "timelength:{4}\ttags:{5}\n" +
            "durl:{6}",
            self.aid,
            self.video_title,
            self.cid,
            self.cid_name,
            self.timelength,
            self.video_tags,
            self.durl[0])


def fetch_bilibili_av(av_number, p):
    """
    用bilibili的av號，fetch B站AV號資料
    """
    log.i('start fetch {}.'.format(av_number))
    req = requests.get(parse.urljoin(
        MAIN_HOST_URL, av_number) + str.format("?p={0}", p), headers=HEADER)
    log.i('request {} finish.'.format(req.url))
    bf = BeautifulSoup(req.text, 'html.parser')
    scripts_tag = bf.find_all("script")
    start_initial = re.escape("window.__INITIAL_STATE__=")
    end_initial = re.escape(
        ";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1])" +
        ".parentNode.removeChild(s);}());")
    start_play = re.escape("window.__playinfo__=")
    as_av_info = Bilibili_file_info()
    for tag in scripts_tag:
        re_initial = re.match(start_initial + "(.+)" +
                              end_initial, str(tag.string))
        re_playinfo = re.match(start_play + "(.+)", str(tag.string))
        m = re_initial if re_initial is not None else re_playinfo
        if m is not None and m is re_initial:
            log.i('__initial_state__ json detected.')
            results = json.loads(m.group(1))
            if len(results["error"]) is 0:
                as_av_info.aid = results["aid"]
                for cid in results["videoData"]["pages"]:
                    as_av_info.cid.append(str(cid["cid"]))
                    as_av_info.cid_name.append(cid["part"])
                for tag in results["tags"]:
                    as_av_info.video_tags.append(tag["tag_name"])
                as_av_info.video_title = results["videoData"]["title"]
                as_av_info.video_desc = results["videoData"]["desc"]
                as_av_info.video_pubdate = results["videoData"]["pubdate"]
                as_av_info.video_pic = results["videoData"]["pic"]
            else:
                log.e('__initial_state__ error: {}'.format(results["error"]))
                raise Exception(results["error"])
        elif m is not None and m is re_playinfo:
            log.i('__playinfo__ json detected.')
            results = json.loads(m.group(1))
            for url in results["durl"]:
                as_av_info.durl.append(url["url"])
            as_av_info.timelength = results["timelength"]
            as_av_info.accept_format = results["accept_format"]
            as_av_info.accept_quality = results["accept_quality"]
            as_av_info.accept_description = results["accept_description"]
    comments_dict = dict()
    log.i('start download comments.')
    for cid in as_av_info.cid:
        comments_dict.update({cid: _cid_comments_list(cid)})
        as_av_info.comments = comments_dict
    if as_av_info.aid is None:
        log.e('target object aid is None.  initial state parse failed.')
        raise Exception(
            "Html parse JSON failed.  INITIAL state can't parse!!  please check {} is correct".format(req.url))
    if len(as_av_info.durl) == 0:
        log.e('target object durl is None.  playinfo parse failed.  please check {} is correct'.format(req.url))
        raise Exception("Html parse JSON failed.  playinfo can't parse!!")
    log.i('fetch bilibili finish.')
    return as_av_info


def _cid_comments_list(cid: str):
    require_link = REALTIME_COMMENT_REQUEST_URL + cid + ".xml"
    req = requests.get(require_link)
    req.encoding = 'utf-8'
    root = ET.fromstring(req.text)
    comment_list = list()
    for child in root:
        if child.tag == "d":
            info = child.attrib["p"].split(",")
            comment_list.append(
                {"user": info[6], "sec": info[0], "text": child.text, "score": None})
    log.i('comment fetch finish {}'.format(require_link))
    return comment_list


def _download_b_video(url, p, cid, aid, no):
    header = HEADER.copy()
    header.update(
        {"Referer": "https://www.bilibili.com/video/av{0}/?p={1}".format(aid, p)})
    with requests.get(url, headers=header, stream=True) as r:
        filename = "{0}-part{1}.flv".format(cid, no)
        log.i("{filename} downloading".format(filename=filename))
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
            log.i('finish download.')

def get_b_comments(aid, p):
    req = requests.get(COMMENT_REQ_URL.format(page=p, aid=aid), headers=HEADER)
    js = json.loads(req.text)
    return_list = list()
    for reply in js["data"]["replies"]:
        comment = dict()
        comment.update({"user":reply["member"]["mid"]})
        comment.update({"text":reply["content"]["message"]})
        comment.update({"like":reply["like"]})
        comment.update({"inline_rcount":reply["rcount"]})
        comment.update({"pub_date":reply["ctime"]})
        return_list.append(comment)
    return return_list


def get_comment_pages_count(aid):
    req = requests.get(COMMENT_REQ_URL.format(page=1, aid=aid), headers=HEADER)
    js = json.loads(req.text)
    pages_c = int()
    try:
        pages_c = (js["data"]["page"]["count"] - 1) // 20
    except KeyError as identifier:
        raise Exception("連接失效")
    return pages_c + 1  # 補餘數
    