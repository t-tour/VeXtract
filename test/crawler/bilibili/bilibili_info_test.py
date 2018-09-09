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
import pytest
import xml.etree.ElementTree as ET

from crawler.bilibili import bilibili

from helper import logger
log = logger.Logger(__name__)

AV_NUMBER_ONE_P = "av23315808"
AV_NUMBER_MANY_P = "av13392824"


def test_fetch_bilibili():
    log.d('start test_fetch_bilibili')
    target = bilibili.fetch_bilibili_av(AV_NUMBER_MANY_P, "1")
    cid_need = ['21945130', '21945131']
    tags_need = ["凹凸世界", "社会摇", "格瑞", "toxic"]
    assert target.aid == "13392824"
    assert [i for i in target.cid if i not in cid_need] == []
    assert target.video_title == "【凹凸世界】瑞骚来袭！手办级渲染第四弹！toxic伪"
    assert [i for i in target.video_tags if i not in tags_need] == []
    assert target.timelength == 110419


def test_j_data_rw():
    log.d('start test_j_data_rw')
    a = bilibili.Bilibili_file_info.load(os.path.join(__root, "test\\test_file\\{}.json".format(AV_NUMBER_ONE_P)))
    assert a.comments[a.cid[0]][0]["score"] == None
    a.comments[a.cid[0]][0]["score"] = 10
    a.save(os.path.join(__root, "test\\test_file\\"))
    b = bilibili.Bilibili_file_info.load(os.path.join(__root, "test\\test_file\\{}.json".format(AV_NUMBER_ONE_P)))
    assert b.comments[b.cid[0]][0]["score"] == 10
    b.comments[b.cid[0]][0]["score"] = None
    b.save(os.path.join(__root, "test\\test_file\\"))
    