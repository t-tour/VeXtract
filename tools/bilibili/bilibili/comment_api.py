import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../"))

import xml.etree.ElementTree as ET
import re
import logging

from bilibili.bilibili.bilibili_info import Bilibili_comment

# TODO: 重構預定
def get_av_comments_list(av, cid="") -> list():
    """
    用av號找尋該影片所有的留言與時軸
    若有多p則必須給cid，不然就會返還
    首個回文資訊
    例外: 未找到指定AV資料夾
    """
    cid = os.listdir(av)[0] if len(cid) == 0 else cid + ".xml"
    tree = ET.parse(av + "/" + cid)
    root = tree.getroot()
    comments = []
    for c in root:
        if c.tag == "d":
            comments.append(Bilibili_comment(
                c.attrib["p"].split(",")[6],
                c.attrib["p"].split(",")[0],
                c.text))
    return comments

if __name__ == "__main__":
    c = get_av_comments_list("av27436999")
    for comment in c:
        print(comment)
