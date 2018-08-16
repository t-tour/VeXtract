import os
import sys
import requests
from urllib import parse
from bs4 import BeautifulSoup
import re
import json
import xml.etree.ElementTree as ET
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../"))

from bilibili.bilibili import bilibili_info as b_info  # noqa

COMMENT_REQUEST_URL = "https://comment.bilibili.com/"
MAIN_HOST_URL = "https://www.bilibili.com/video/"


def fetch_bilibili_av(av_number, p=1) -> b_info.Bilibili_file_info():
    """
    用bilibili的av號，fetch B站AV號資料
    """
    m = re.match('av[0-9]+', av_number)
    if m is None:
        raise Exception("av號格式錯誤")
    av_number = m.group(0)
    req = requests.get(parse.urljoin(
        MAIN_HOST_URL, av_number) + str.format("?p={0}", p))
    bf = BeautifulSoup(req.text, 'html.parser')
    scripts_tag = bf.find_all("script")
    start_initial = re.escape("window.__INITIAL_STATE__=")
    end_initial = re.escape(
        ";(function(){var s;(s=document.currentScript||document.scripts[document.scripts.length-1])" +
        ".parentNode.removeChild(s);}());")
    start_play = re.escape("window.__playinfo__=")
    as_av_info = b_info.Bilibili_file_info()
    for tag in scripts_tag:
        r1 = re.match(start_initial + "(.+)" + end_initial, str(tag.string))
        r2 = re.match(start_play + "(.+)", str(tag.string))
        m = r1 if r1 is not None else r2
        if m is not None and m is r1:
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
                raise Exception(results["error"])
        elif m is not None and m is r2:
            results = json.loads(m.group(1))
            for url in results["durl"]:
                as_av_info.durl.append(url["url"])
            as_av_info.timelength = results["timelength"]
            as_av_info.accept_format = results["accept_format"]
            as_av_info.accept_quality = results["accept_quality"]
            as_av_info.accept_description = results["accept_description"]
    comments_dict = dict()
    for cid in as_av_info.cid:
        comments_dict.update({cid: __cid_comments_list(cid)})
        as_av_info.comments = comments_dict
    if as_av_info.aid is None:
        raise Exception("Html parse JSON failed.  INITIAL state can't parse!!")
    if as_av_info.durl[0] is None:
        raise Exception("Html parse JSON failed.  playinfo can't parse!!")
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
                {"user": info[6], "sec": info[0], "text": child.text, "score": comment_score(child.text)})
    return comment_list



def comment_score(text):
    return 1

def cid_xml_file(cid: str):
    """
    用cid在目錄下寫入檔案(cid).xml
    """
    fd_name = cid + ".xml"
    req = requests.get(COMMENT_REQUEST_URL + fd_name)
    req.encoding = 'utf-8'
    with open(fd_name, 'w', encoding="utf-8") as f:
        f.write(req.text)


def get_comment_data(av_number: str, store="chat_xml_res/") -> b_info.Bilibili_file_info():
    """
    可以下載xml檔案給api讀取
    預設目錄是 current work dir 的 chat_xml_res/
    """
    my_path = os.getcwd()
    try:
        os.mkdir(store)
    except FileExistsError:
        pass
    b = fetch_bilibili_av(av_number)
    os.chdir(store)
    os.mkdir(av_number)
    os.chdir(av_number)
    for req_cid in b.cid:
        cid_xml_file(req_cid)
    os.chdir(my_path)


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
            print("正在下載av:cid av{0}:{1} :3 名稱:{2}".format(
                parted_target.aid, cid, cid_name))
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
        print("正在下載av:cid av{0}:{1} :3 名稱:{2}".format(
            target.aid, target.cid[p - 1], target.cid_name[p - 1]))
        for no, url, in zip(range(len(target.durl)), target.durl):
            __download_b_video(url, p, target.cid[p - 1], target.aid, no)
    os.chdir(my_path)


def __download_b_video(url, p, cid, aid, no, log_level=0):
    header = {"user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/67.0.3396.99 Safari/537.36"),
              "Referer": "https://www.bilibili.com/video/av{0}/?p={1}".format(aid, p),
              "origin": "https://www.bilibili.com"}
    with requests.get(url, headers=header, stream=True) as r:
        filename = "{0}-{1}.flv".format(cid, no)
        if log_level >= 1:
            print("{filename} downloading".format(filename=filename), end="")
        with open(filename, "wb") as f:
            c = 0
            for chunk in r.iter_content(chunk_size=1024):
                c += 1
                # FIXME: 在b_info中增加各檔案大小的屬性 就可以透過chunk_size辨別進度!  現在先這樣
                # \r可以吃掉為卵的餅乾
                if c >= 1024:
                    if log_level >= 1:
                        print(".", end="")
                    sys.stdout.flush()
                    c = 0
                f.write(chunk)
            if log_level >= 1:
                print("finish")


def __safe_makedir(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


if __name__ == "__main__":
    # get_video_data("av25233957")
    # print(fetch_bilibili_av("av13392824"))
    a = fetch_bilibili_av("av28707590")
    a.fetch_comment_score()
    

    print(b)
