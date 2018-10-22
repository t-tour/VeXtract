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


from crawler.bilibili import bilibili
from analyzer.algorithm import segment_generator
from generator.video import video_process


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
    segments = segment_generator.generate_segments(video)
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
    segments_list = sorted(segments_list, key=lambda foo: foo[0])
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
    b_info = bilibili.info_crawler(URL)
    print(b_info)
    print(b_info.comments)
    
    # VIDEO_PATH = os.path.join(
    #     __root, "file\\crawler\\bilibili\\av{}\\{}.flv".format(b_info.aid, b_info.cid[0]))
    # b_info.save(os.path.join(__root, "file\\algorithm\\"))
    # wanted_tuple_list = count_wanted_length(
    #     600, VIDEO_PATH, b_info.comments[b_info.cid[0]])
    # wanted_tuple_list = sorted(wanted_tuple_list, key=lambda i: i[0])
    # segs = segment_generator.generate_segments(VIDEO_PATH)
    # graded_segs = _grade_segments(segs, b_info.comments[b_info.cid[0]])
    # vp.video_process(VIDEO_PATH, wanted_tuple_list, True, "ten_min.mp4")
