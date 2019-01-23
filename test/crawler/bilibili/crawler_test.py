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
_ROOT = __root

from helper import logger
log = logger.Logger(__name__)

from crawler.bilibili.crawler import BilibiliCrawler

URL = "https://www.bilibili.com/video/av2927640"
URL_MANYP = "https://www.bilibili.com/video/av13392824/?p=2&spm_id_from=333.334.b_686f6d655f706f70756c6172697a65.3"
INCORRECT_URL = "https://instantiated.bilibili.com/video/av5445554"

CRAWLER = BilibiliCrawler(URL)

def test_crawler_init():
    _ = BilibiliCrawler(URL)


def test_info_crawler():
    info = CRAWLER.info_crawler()
    assert info.videoname == "听说大家都在看夏洛特，那我们就一起来愉快的吐槽它吧P1_"
    assert info.uploader == "LexBurner"
    assert info.videoid == "av2927640_4580586"


def test_file_crawler():
    file_ = CRAWLER.file_crawler()
    # TODO: Implement Request.
    raise NotImplementedError
