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

from crawler import bilibili
from analyzer.algorithm import video_algorithm


def __generate_segments(video):
    """
    隨意產生OAO
    """
    log.i('Start generate_segments with {}'.format(video))
    video_length = video_algorithm.get_video_length(video)
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


def __grade_segments(segments, real_time_comments=None, comments=None, audio=None, video=None):
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
        if real_time_comments:
            for comment in real_time_comments:
                if comment["time"] >= segment[0] and comment["time"] < segment[1]:
                    total_score += 1
        graded_list.append({
            "time": segment,
            "total_score": total_score
        })
    log.i('grade_list is: {}'.format(graded_list))
    return graded_list


def wanted_length(length, video, real_time_comments=None, comments=None):
    """
    回傳應該要剪的片段
    length: 總時長不超過 length
    video: 影片位置
    """
    segments = __generate_segments(video)
    segments_graded = __grade_segments(segments, real_time_comments)
    segments_graded = sorted(
        segments_graded, key=lambda segment: segment["total_score"], reverse=True)
    segments_list = list()
    total_length = 0
    for segment in segments_graded:
        segments_list.append(segment["time"])
        total_length += segment["time"][1] - segment["time"][0]
        if total_length > length:
            segments_list.pop()
            break
    log.i('segments_list: {}'.format(segments_list))
    return segments_list


def wanted_grade_above(grade, video, comments):
    """
    回傳應該要剪的片段
    grade: 分數高於 grade 就收錄
    video: 影片位置
    """
    raise Exception("還沒實作拉")
    return None


if __name__ == "__main__":
    log.i('time_tagger Start!')
    print(__root + "file\\crawler\\av30199696\\1_52660766\\52660766-part0.flv")
    b_info = bilibili.fetch_bilibili_av("av30199696")
    real_time_comments = list()
    for comment in b_info.comments["52660766"]:
        real_time_comments.append(
            {"time": float(comment.sec), "text": comment.text})
    # print(real_time_comments)
    os.chdir(__root + "file\\crawler\\av30199696\\1_52660766\\")
    wanted_length(
        100, "\"" + __root + "file\\crawler\\av30199696\\1_52660766\\52660766-part0.flv\"", real_time_comments)
