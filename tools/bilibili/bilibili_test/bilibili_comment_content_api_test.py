import sys
import os
import pytest
import xml.etree.ElementTree as ET
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../"))

from danmaku.bilibili import bilibili_comment_content_api as bci  # noqa


AV_NUMBER_ERROR_FORMATTING = "aa12345666d"
AV_NUMBER_NULL = "av2"
AV_NUMBER_ONE_P = "av23315808"
AV_NUMBER_MANY_P = "av13392824"
CID = '38842914'


def test_fetch_bilibili_with_error_formatting():
    with pytest.raises(Exception, match=r'av號格式錯誤'):
        bci.fetch_bilibili_av(AV_NUMBER_ERROR_FORMATTING)


def test_fetch_bilibili_with_not_found_error():
    with pytest.raises(Exception, match=r'.*40[34].*'):
        bci.fetch_bilibili_av(AV_NUMBER_NULL)


def test_fetch_bilibili():
    target = bci.fetch_bilibili_av(AV_NUMBER_MANY_P)
    cid_need = ['21945130', '21945131']
    tags_need = ["凹凸世界", "社会摇", "格瑞", "toxic"]
    assert target.aid == "13392824"
    assert [i for i in target.cid if i not in cid_need] == []
    assert target.video_title == "【凹凸世界】瑞骚来袭！手办级渲染第四弹！toxic伪"
    assert [i for i in target.video_tags if i not in tags_need] == []
    assert target.timelength == 110419


def test_cid_xml_file():
    CID_PATH = CID + ".xml"
    bci.cid_xml_file(CID)
    tree = ET.parse(CID_PATH)
    root = tree.getroot()
    os.remove(CID_PATH)
    assert root[1].text == "38842914"


def test_get_comment_data():
    bci.get_comment_data(
        AV_NUMBER_MANY_P, os.path.dirname(__file__) + "/chat_xml_res")
    os.chdir(os.path.dirname(__file__) + "/chat_xml_res")
    os.chdir(AV_NUMBER_MANY_P)
    need = ['21945130.xml', '21945131.xml']
    now = os.listdir(".")
    assert [i for i in now if i not in need] == []
    for rm in os.listdir('.'):
        os.remove(rm)
    os.chdir('../')
    os.rmdir(AV_NUMBER_MANY_P)
    os.chdir('../')
    os.rmdir('chat_xml_res')
