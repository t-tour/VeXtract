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

from urllib import parse
import re
import json
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

from crawler.bilibili.bilibili_info import Bilibili_file_info,\
    fetch_bilibili_av, _download_b_video, get_b_comments, get_comment_pages_count
from generator.video import video_contact


def _url_parse(url):
    url_parsed = parse.urlsplit(url)
    return_value = dict()
    if len(url_parsed.query) > 0:
        for part in url_parsed.query.split("&"):
            key = part.split("=")[0]
            value = part.split("=")[1]
            return_value.update({key: value})
    return_value.update({"avnumber": url_parsed.path.split("/")[2]})
    try:
        _ = return_value["p"]
    except KeyError:
        return_value.update({"p": "1"})
    m = re.match('av[0-9]+', return_value["avnumber"])
    if m is None:
        log.e('av_number mismatch \'{}\''.format(return_value["avnumber"]))
        raise Exception("av號格式錯誤")
    return return_value


def file_crawler(url, des=os.path.join(__root, "file", "crawler", "bilibili")):
    """
    下載影片檔案
    url: b站影片網址
    des: 儲存位置
    -> None
    """
    url_info = _url_parse(url)
    p = int(url_info["p"])
    target = fetch_bilibili_av(url_info["avnumber"], p)
    des = os.path.join(des, "av" + target.aid)
    os.makedirs(des, exist_ok=True)
    log.i("正在下載 av{0}_{1} cid名稱:{2}".format(
        target.aid, target.cid[p-1], target.cid_name[p-1]))
    for no, url in zip(range(len(target.durl)), target.durl):
        _download_b_video(url, p, target.cid[p-1], target.aid, no)
    concat_list = [i for i in os.listdir(
        ".") if re.match(r"^\d+-part\d+.flv$", i)]
    video_contact.contact_by_manifest(
        concat_list, des, target.cid[p-1])
    for concats in concat_list:
        os.remove(concats)


def real_time_comments_crawler(url):
    """
    獲取影片資料
    url: b站影片網址

    -> {
        user: 
        sec: 在影片上評論的時間  ps. 不是pubtime
        text: 
        score: default none
    }
    """
    url_info = _url_parse(url)
    target = fetch_bilibili_av(url_info["avnumber"], url_info["p"])
    return target.comments[target.cid[int(url_info["p"])-1]]


def info_crawler(url, des=os.path.join(__root, "file", "crawler", "bilibili"), save=False):
    """
    獲取影片資料
    url: b站影片網址
    des: 儲存位置
    save: 是否儲存
    -> Bilibili_file_info
    """
    url_info = _url_parse(url)
    info = fetch_bilibili_av(url_info["avnumber"], url_info["p"])
    if save:
        des = os.path.join(des, "{id}").format(
            id=url_info["avnumber"])
        os.makedirs(des, exist_ok=True)
        info.save(des)
    return info


def comment_crawler(url):
    """
    獲取影片回復
    url: b站影片網址
    - > {
        user:
        text:
        like: 喜歡數量
        inline_rcount: 回覆這篇回覆的數量
        pub_date: 發文日期
    }
    """
    url_info = _url_parse(url)
    aid = url_info["avnumber"][2::]
    pages = get_comment_pages_count(aid) + 1
    return_comments_list = list()
    for i in range(1,  pages):
        a = get_b_comments(aid, i)
        return_comments_list += a
    return return_comments_list


if __name__ == "__main__":
    # get_video_data("av25233957")
    # print(fetch_bilibili_av("av13392824"))
    # a.fetch_comment_score(test=True, limitation=5000)
    # a.save()
    # b = fetch_bilibili_av("av29311976")
    # b.fetch_comment_score(limitation=5000)
    # b.save()
    a = info_crawler(
        "https://www.bilibili.com/video/av25219896?from=search&seid=16811196391356959694")
    print()
