import sys
sys.path.append(__file__ + '/..' * (len(__file__.split('\\')) -
                                    __file__.split('\\').index('VeXtract') - 1))
import os
import requests
from urllib import parse
from bs4 import BeautifulSoup
import re
import json
import xml.etree.ElementTree as ET

from tools.bilibili import bilibili_info as b_info  # noqa
from helper import logger
log = logger.Logger(__name__)
log.set_level('i')

COMMENT_REQUEST_URL = "https://comment.bilibili.com/"
MAIN_HOST_URL = "https://www.bilibili.com/video/"


def fetch_bilibili_av(av_number, p=1) -> b_info.Bilibili_file_info():
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
    as_av_info = b_info.Bilibili_file_info()
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
    b.aid = 222222213
    b.save()
