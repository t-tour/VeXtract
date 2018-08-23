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

from crawler import bilibili

from helper import logger
log = logger.Logger(__name__)

AV_NUMBER_ERROR_FORMATTING = "aa12345666d"
AV_NUMBER_NULL = "av2"
AV_NUMBER_ONE_P = "av23315808"
AV_NUMBER_MANY_P = "av13392824"
CID = '38842914'


def test_fetch_bilibili_with_error_formatting():
    log.d('start test_fetch_bilibili_with_error_formatting')
    with pytest.raises(Exception, match=r'av號格式錯誤'):
        bilibili.fetch_bilibili_av(AV_NUMBER_ERROR_FORMATTING)


def test_fetch_bilibili_with_not_found_error():
    log.d('start test_fetch_bilibili_with_not_found_error')
    with pytest.raises(Exception, match=r'.*40[34].*'):
        bilibili.fetch_bilibili_av(AV_NUMBER_NULL)


def test_fetch_bilibili():
    log.d('start test_fetch_bilibili')
    target = bilibili.fetch_bilibili_av(AV_NUMBER_MANY_P)
    cid_need = ['21945130', '21945131']
    tags_need = ["凹凸世界", "社会摇", "格瑞", "toxic"]
    assert target.aid == "13392824"
    assert [i for i in target.cid if i not in cid_need] == []
    assert target.video_title == "【凹凸世界】瑞骚来袭！手办级渲染第四弹！toxic伪"
    assert [i for i in target.video_tags if i not in tags_need] == []
    assert target.timelength == 110419


def test_j_data_rw_and_score_analyzer():
    log.d('start test_j_data_rw_and_score_analyzer')
    os.chdir(__root + "test/test_file/")
    a = bilibili.Bilibili_file_info.load("{}.json".format(AV_NUMBER_ONE_P))
    assert a.comments[a.cid[0]][0].score == None
    a.fetch_comment_score(limitation=5000)
    assert a.comments[a.cid[0]][0].score == 10
    a.save()
    b = bilibili.Bilibili_file_info.load("{}.json".format(AV_NUMBER_ONE_P))
    for comment in b.comments[a.cid[0]]:
        comment.score = None
    b.save()
