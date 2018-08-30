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

import numpy
import matplotlib.pyplot as plt

from analyzer.algorithm import time_tagger
from crawler import bilibili

print(sys.argv)

segments = time_tagger.__generate_segments("\"" + __root + "file\\crawler\\av30199696\\1_52660766\\52660766-part0.flv\"")
b_info = bilibili.fetch_bilibili_av("av30199696")
print(len(b_info.comments[b_info.cid[0]]))
real_time_comments = list()
for comment in b_info.comments["52660766"]:
    real_time_comments.append(
        {"time": float(comment.sec), "text": comment.text})
segments_graded = time_tagger.__grade_segments(segments,real_time_comments)
x = [i["time"][0] for i in segments_graded]
y = [i["total_score"] for i in segments_graded]
plt.plot(x,y)
plt.show()