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
import os
import requests
from urllib import parse
from bs4 import BeautifulSoup
import re
import json
import xml.etree.ElementTree as ET


from analyzer.text import natural_lang_process
from helper import logger
log = logger.Logger(__name__)
log.set_level('i')

COMMENT_REQUEST_URL = "https://comment.bilibili.com/"
MAIN_HOST_URL = "https://www.bilibili.com/video/"


class Bilibili_file_info():
    aid: str()
    cid: list()
    cid_name: list()
    timelength: int()
    accept_format: list()
    accept_quality: list()
    accept_quailty_description: list()
    video_title: str()
    video_desc: str()
    video_pubdate: int()
    video_pic: str()
    video_tags: list()
    durl: list()
    __comments: dict()

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, value):
        for cid, comments in value.items():
            b_comments_list = list()
            for comment in comments:
                b_comment = Bilibili_comment(
                    comment["user"], comment["sec"], comment["text"])
                b_comment.score = comment["score"]
                b_comments_list.append(b_comment)
            self.__comments.update({cid: b_comments_list})

    def get_pages_count(self):
        return len(self.cid)

    def save(self):
        with open('av{}.json'.format(self.aid), 'w', encoding='utf-8') as f:
            json.dump(self, f, default=lambda o: o.__dict__,
                      ensure_ascii=False)
        log.i('av{}.json saved'.format(self.aid))

    @staticmethod
    def load(j_data):
        with open(j_data, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            obj = Bilibili_file_info()
            # FIXME: load 的時候 comment 也必須用 satter 才行
            for attr, value in loaded.items():
                obj.__setattr__(attr, value)
                if attr == "_Bilibili_file_info__comments":
                    obj.comments = value
        log.i('load {} finish.'.format(j_data))
        return obj

    def fetch_comment_score(self, test=True, limitation=100):
        """
        default: test=True, limitation=100
        test: 測試模式，分數全為10
        limitation: 最大comment上限，包含所有cid
        """
        total_len = 0
        for cid in self.cid:
            total_len += len(self.comments[cid])
        if total_len > limitation:
            raise Exception("comments up to limitation!!")
        for cid in self.cid:
            for comment in self.comments[cid]:
                if test:
                    comment.score = 10
                else:
                    comment.score = natural_lang_process.text_analyze(comment.text)
        log.i('av{} fetch comment finish.'.format(self.aid))
        

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
        self.__comments = dict()

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


class Bilibili_comment():
    user: str()
    sec: float()
    text: str()
    score: float()

    def __init__(self, user, sec, text):
        self.user = user
        self.sec = sec
        self.text = text
        self.score = None

    def __str__(self):
        return str.format("user:{0}\ttime:{1}\tscore:{3}\t{2}",
                          self.user, self.sec, self.text, self.score)

    def __repr__(self):
        return self.__str__() + "\n"


def fetch_bilibili_av(av_number, p=1) -> Bilibili_file_info():
    """
    用bilibili的av號，fetch B站AV號資料
    """
    log.i('start fetch bilibili.')
    m = re.match('av[0-9]+', av_number)
    if m is None:
        log.e('av_number mismatch \'{}\''.format(av_number))
        raise Exception("av號格式錯誤")
    av_number = m.group(0)
    req = requests.get(parse.urljoin(
        MAIN_HOST_URL, av_number) + str.format("?p={0}", p))
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
        comments_dict.update({cid: __cid_comments_list(cid)})
        as_av_info.comments = comments_dict
    if as_av_info.aid is None:
        log.e('target object aid is None.  initial state parse failed.')
        raise Exception("Html parse JSON failed.  INITIAL state can't parse!!")
    if as_av_info.durl[0] is None:
        log.e('target object durl is None.  playinfo parse failed.')
        raise Exception("Html parse JSON failed.  playinfo can't parse!!")
    log.i('fetch bilibili finish.')
    return as_av_info


def __cid_comments_list(cid: str) -> list():
    fd_name = cid + ".xml"
    req = requests.get(COMMENT_REQUEST_URL + fd_name)
    req.encoding = 'utf-8'
    root = ET.fromstring(req.text)
    comment_list = list()
    for child in root:
        if child.tag == "d":
            info = child.attrib["p"].split(",")
            comment_list.append(
                {"user": info[6], "sec": info[0], "text": child.text, "score": None})
    return comment_list


def get_video_data(avnumber, p=-1, store="video_res/", known=None):
    """
    獲取影片資料
    """
    my_path = os.getcwd()
    __safe_makedir(store)
    os.chdir(store)
    __safe_makedir(avnumber)
    os.chdir(avnumber)
    if p is -1:
        target = fetch_bilibili_av(avnumber) if known is None else known
        for p, cid, cid_name in zip(range(1, target.get_pages_count() + 1), target.cid, target.cid_name):
            parted_target = fetch_bilibili_av(avnumber, p)
            __safe_makedir(str(cid))
            os.chdir(str(cid))
            # FIXME: 檔名紀錄log等修復
            log.i("正在下載av:cid av{0}:{1} :3 名稱:{2}".format(
                parted_target.aid, cid, "名稱不可用"))
            for no, url in zip(range(len(parted_target.durl)), parted_target.durl):
                # 測試代碼這裡
                # print("{0}-{1}.flv downloading.....finish".format(cid, no))
                # with open("{0}test_{1}".format(cid, no), "w") as f:
                #     f.write("dd")
                __download_b_video(url, p, cid, target.aid, no)
            os.chdir("..")
    else:
        target = fetch_bilibili_av(avnumber) if known is None else known
        # referenced before assignment 指定錯誤的p數
        __safe_makedir(str(target.cid[p - 1]))
        os.chdir(str(target.cid[p - 1]))
        log.i("正在下載av:cid av{0}:{1} :3 名稱:{2}".format(
            target.aid, target.cid[p - 1], target.cid_name[p - 1]))
        for no, url, in zip(range(len(target.durl)), target.durl):
            __download_b_video(url, p, target.cid[p - 1], target.aid, no)
    os.chdir(my_path)


def __download_b_video(url, p, cid, aid, no):
    header = {"user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/67.0.3396.99 Safari/537.36"),
              "Referer": "https://www.bilibili.com/video/av{0}/?p={1}".format(aid, p),
              "origin": "https://www.bilibili.com"}
    with requests.get(url, headers=header, stream=True) as r:
        filename = "{0}-{1}.flv".format(cid, no)
        log.i("{filename} downloading".format(filename=filename))
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
            log.i('finish download.')


def __safe_makedir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

if __name__ == "__main__":
    # get_video_data("av25233957")
    # print(fetch_bilibili_av("av13392824"))
    # a.fetch_comment_score(test=True, limitation=5000)
    # a.save()
    b = fetch_bilibili_av("av29311976")
    b.fetch_comment_score(limitation=5000)
    b.save()
    a = Bilibili_file_info.load("av29311976.json")
    print(a)