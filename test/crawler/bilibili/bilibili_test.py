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

from helper import logger
log = logger.Logger(__name__)

import shutil
import re

import pytest

from crawler.bilibili import bilibili

URL = "https://www.bilibili.com/video/av34188644"
URL_WITH_P = "https://www.bilibili.com/video/av25174054/?p=5"
URL_WITH_ERROR = "https://gitlab.com/T-tour/VeXtract/network/master"


def test_info_crawler():
    log.i('start test_info_crawler:')
    a = bilibili.info_crawler(URL)
    assert a.video_title == "校花投怀送抱，屌丝却无动于衷，原因竟如此不忍直视...2018最让人瞎眼的动画"


def test_info_crawler_save_destination():
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
    item = a.pop()
    assert (item['text'] != None) & (item['text'] != "")
    assert re.match(r'\d+\.\d+', item['sec']) != None

def test_real_time_comment_crawler_with_p():
    log.i('start test_real_time_comment_crawler.')
    a = bilibili.real_time_comments_crawler(URL_WITH_P)
    item = a.pop()
    assert (item['text'] != None) & (item['text'] != "")
    assert re.match(r'\d+\.\d+', item['sec']) != None


def test_url_parse():
    log.i('start test__url_parse.')
    a = bilibili._url_parse(URL)
    assert a["avnumber"] == "av34188644"
    assert a["p"] == "1"


def test_url_parse_with_p():
    log.i('start test__url_parse_with_p')
    a = bilibili._url_parse(URL_WITH_P)
    assert a["avnumber"] == "av25174054"
    assert a["p"] == "5"


def test_url_parse_with_error():
    log.i('start test__url_parse_with_error')
    with pytest.raises(Exception, match=r'av號格式錯誤'):
        bilibili._url_parse(URL_WITH_ERROR)

# ignore this: 花太多時間了
def no_test_comment_crawler():
    log.i('start test_comment_crawler.')
    a = bilibili.comment_crawler(URL)
    a = sorted(a, key=lambda c: c["pub_date"])
    assert a[0]["user"] == "19478213"
    assert a[0]["text"] == "看到进度条差点被吓出来，不过还是坚持下来了"
