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

import subprocess

from crawler.bilibili import bilibili, bilibili_info
from analyzer.algorithm import video_algorithm


def _generate_segments(video):
    """
    隨意產生OAO
    """
    log.i('Start generate_segments with {}'.format(video))
    video_length = video_algorithm.get_video_length(video)
    video_length = int(video_length*1000)
    sep = 5000
    

    segments_list = list()
    for i in range(0, video_length, sep):
        if i+sep > video_length:
            segments_list.pop()
            segments_list.append(((i-sep)/1000, (video_length)/1000))
            continue
        segments_list.append((i/1000, (i+sep)/1000))
    log.i('sements_list is: {}'.format(segments_list))
    return segments_list


def _grade_segments(segments, real_time_comments=None, comments=None, audio=None, video=None):
    """
    segments: 切分的影片片段p
    real_time_comments, comments, audio, video: 評分用的資料
    list
    {
        time: (start_time, end_time),
        total_score: score
    },{}...
    """
    log.i('Start grade segments.')
    graded_list = list()
    for segment in segments:
        total_score = 0
        # 對 real_time_comments 做評分
        if real_time_comments:
            for comment in real_time_comments:
                if float(comment["sec"]) >= segment[0] and float(comment["sec"]) < segment[1]:
                    if comment["score"]:
                        total_score += float(comment["score"]) * 10 + 1
                    else:
                        total_score += 3
        # 對 comments 做評分
        if comments:
            pass
        if audio:
            pass
        if video:
            pass
        graded_list.append({
            "sec": segment,
            "total_score": total_score
        })
    log.i('grade_list is: {}'.format(graded_list))
    return graded_list


def count_wanted_length(length, video, real_time_comments=None, comments=None):
    """
    回傳應該要剪的片段
    length: 總時長不超過 length
    video: 影片位置
    """
    segments = _generate_segments(video)
    segments_graded = _grade_segments(segments, real_time_comments)
    segments_graded = sorted(
        segments_graded, key=lambda segment: segment["total_score"], reverse=True)
    segments_list = list()
    total_length = 0
    for segment in segments_graded:
        segments_list.append(segment["sec"])
        total_length += segment["sec"][1] - segment["sec"][0]
        if total_length > length:
            segments_list.pop()
            break
    log.i('segments_list: {}'.format(segments_list))
    segments_list = sorted(segments_list, key=lambda foo: foo["start_time"])
    return segments_list


def count_wanted_grade_above(grade, video, comments):
    """
    回傳應該要剪的片段
    grade: 分數高於 grade 就收錄
    video: 影片位置
    """
    raise Exception("還沒實作拉")
    return None


if __name__ == "__main__":
    from generator.video import video_process as vp
    from analyzer.text import natural_lang_process
    log.i('time_tagger Start!')
    URL = "https://www.bilibili.com/video/av8733186?from=search&seid=4119483458303784416"
    b_info = bilibili.Bilibili_file_info.load(
        os.path.join(__root, "av8733186.json"))
    VIDEO_PATH = os.path.join(
        __root, "file\\crawler\\bilibili\\av{}\\{}.flv".format(b_info.aid, b_info.cid[0]))
    b_info.save(os.path.join(__root, "file\\algorithm\\"))
    wanted_tuple_list = count_wanted_length(
        600, VIDEO_PATH, b_info.comments[b_info.cid[0]])
    wanted_tuple_list = sorted(wanted_tuple_list, key=lambda i: i[0])
    segs = _generate_segments(VIDEO_PATH)
    graded_segs = _grade_segments(segs, b_info.comments[b_info.cid[0]])
    vp.video_process(VIDEO_PATH, wanted_tuple_list, True, "ten_min.mp4")

"""
    from matplotlib import pyplot as pt
    pt.figure(1)
    pt.subplot(211).set_title("abs value")
    pt.plot(range(5, int(b_info.timelength/1000), 5),
            [i["total_score"] for i in graded_segs])
    pt.xlabel("time")
    pt.ylabel("score")
    pt.subplot(212).set_title("avs value(K)")
    y = 0
    y_ax = list()
    for i, graded_seg in zip(range(len(graded_segs)), graded_segs):
        y += graded_seg["total_score"]
        if i < 5:
            opt = y/(i+1)
        else:
            y -= graded_segs[i-5]["total_score"]
            opt = y/5
        y_ax.append(opt)
    pt.plot(range(5, int(b_info.timelength/1000), 5), y_ax)
    pt.ylim([0,25])
    pt.xlabel("time")
    pt.ylabel("25s avs score")
    pt.show()
"""

    # 做裁剪
    # vp.video_process(VIDEO_PATH, wanted_tuple_list, temp_Keep=True, output_name="ss")
