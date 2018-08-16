import sys
import os
import pytest
import logging
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/../../"))

from danmaku.bilibili import comment_api  # noqa

logger = logging.getLogger(__name__)
NULL_PATH = "02D20BBD7E394A/"
XML_PATH = 'xml_res_for_testing/'
AV_NUMBER = "av27436999"


def test_get_av_comments_list():
    os.chdir(os.path.dirname(__file__) + "/" + XML_PATH)
    logger.warning(os.path.dirname(__file__) + str(os.listdir(".")))
    logger.warning(os.listdir(AV_NUMBER)[0])
    x = comment_api.get_av_comments_list(AV_NUMBER)
    assert x[1].user == "9ee3cac2"
