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

import shutil

import pytest

from crawler.bilibili import bilibili

URL = "https://www.bilibili.com/video/av5275610"
URL_WITH_P = "https://www.bilibili.com/video/av5275610?p=5"
URL_WITH_ERROR = "https://gitlab.com/T-tour/VeXtract/network/master"


def test_info_crawler():
    log.i('start test_info_crawler:')
    a = bilibili.info_crawler(URL)
    assert a.video_title == "逝影绝忧伪声课堂第七轮"


def test_info_crawler_save_des():
    log.i('start test_info_crawler_save.')
    des = os.path.join(__root, "test\\test_file\\")
    a = bilibili.info_crawler(URL, des, save=True)
    b = bilibili.Bilibili_file_info.load(
        des + "av{aid}\\av{aid}.json".format(aid=a.aid))
    assert sorted(a.cid) == sorted(b.cid)
    shutil.rmtree(des + "av{aid}".format(aid=b.aid))


def test_real_time_comment_crawler():
    log.i('start test_real_time_comment_crawler.')
    a = bilibili.real_time_comments_crawler(URL)
    comp_list = sorted(a, key=lambda d: d["user"])
    comp = {'user': '159ab093', 'sec': '579.79500',
            'text': '18年清明节留', 'score': None}
    assert comp == comp_list[0]


def test_url_parse():
    log.i('start test__url_parse.')
    a = bilibili._url_parse(URL)
    assert a["avnumber"] == "av5275610"
    assert a["p"] == "1"


def test_url_parse_with_p():
    log.i('start test__url_parse_with_p')
    a = bilibili._url_parse(URL_WITH_P)
    assert a["avnumber"] == "av5275610"
    assert a["p"] == "5"


def test_url_parse_with_error():
    log.i('start test__url_parse_with_error')
    with pytest.raises(Exception, match=r'av號格式錯誤'):
        bilibili._url_parse(URL_WITH_ERROR)
        