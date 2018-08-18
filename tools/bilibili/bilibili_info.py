import sys
sys.path.append(__file__ + '/..' * (len(__file__.split('\\')) -
                                    __file__.split('\\').index('VeXtract') - 1))

import json

from tools.analyzer.text_sentiment_analyze import text_analyze
from helper import logger
log = logger.Logger(__name__)

class Bilibili_file_info():
    aid: str()
    cid: list()
    cid_name: list()
    timelength: int()
    accept_format: list()
    accept_quality: list()
    accept_quailty_description: list()
    video_title: str()
    video_desc: str()
    video_pubdate: int()
    video_pic: str()
    video_tags: list()
    durl: list()
    __comments: dict()

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, value):
        for cid, comments in value.items():
            b_comments_list = list()
            for comment in comments:
                b_comment = Bilibili_comment(
                    comment["user"], comment["sec"], comment["text"])
                b_comment.score = comment["score"]
                b_comments_list.append(b_comment)
            self.__comments.update({cid: b_comments_list})

    def get_pages_count(self):
        return len(self.cid)

    def save(self):
        with open('av{}.json'.format(self.aid), 'w', encoding='utf-8') as f:
            json.dump(self, f, default=lambda o: o.__dict__,
                      ensure_ascii=False)
        log.i('av{}.json saved'.format(self.aid))

    @staticmethod
    def load(j_data):
        with open(j_data, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            obj = Bilibili_file_info()
            for attr, value in loaded.items():
                obj.__setattr__(attr, value)
        log.i('load {} finish.'.format(j_data))
        return obj

    def fetch_comment_score(self, test=True, limitation=100):
        """
        default: test=True, limitation=100
        test: 測試模式，分數全為10
        limitation: 最大comment上限，包含所有cid
        """
        total_len = 0
        for cid in self.cid:
            total_len += len(self.comments[cid])
        if total_len > limitation:
            raise Exception("comments up to limitation!!")
        for cid in self.cid:
            for comment in self.comments[cid]:
                if test:
                    comment["score"] = 10
                else:
                    comment["score"] = text_analyze(comment.text)
        log.i('av{} fetch comment finish.'.format(self.aid))
        

    def __init__(self):
        self.aid = None
        self.cid = list()
        self.cid_name = list()
        self.timelength = 0
        self.accept_format = list()
        self.accept_quality = list()
        self.accept_quailty_description = list()
        self.video_title = None
        self.video_desc = None
        self.video_pubdate = None
        self.video_pic = None
        self.video_tags = list()
        self.durl = list()
        self.__comments = dict()

    def __str__(self):
        return str.format(
            "aid:{0}\tvideo_title:{1}\n" +
            "cid:{2}\tcid_title:{3}"
            "timelength:{4}\ttags:{5}\n" +
            "durl:{6}",
            self.aid,
            self.video_title,
            self.cid,
            self.cid_name,
            self.timelength,
            self.video_tags,
            self.durl[0])


class Bilibili_comment():
    user: str()
    sec: float()
    text: str()
    score: float()

    def __init__(self, user, sec, text):
        self.user = user
        self.sec = sec
        self.text = text
        self.score = None

    def __str__(self):
        return str.format("user:{0}\ttime:{1}\tscore:{3}\t{2}",
                          self.user, self.sec, self.text, self.score)

    def __repr__(self):
        return self.__str__() + "\n"


if __name__ == "__main__":
    input = {"aid": 12355, "cid": 5555, "quality": ["720p60", "720", "480"]}
