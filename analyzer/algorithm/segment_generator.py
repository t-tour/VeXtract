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

from generator.video import video_process
from analyzer.audio import fake_analyzer

def generate_segments(video, minimum_length=5000, vocal_frequency_range=(15, 30), trigger=0.3, stability="Not Use Now"):
    """
    video:影片
    minimum_length:最小長度 milisecond
    vocal_frequency_range:人聲判定範圍
    trigger:觸發人聲平均
    stability:防止彈跳
    """
    log.i('Start generate_segments with {}'.format(video))

    # video轉聲訊
    video_name = "".join(video.split(os.sep)[-1].split(".")[0:-1])
    video_process.video_encoding(video, os.path.join(
        __root, "file", "generator"), video_name + ".wav", ifMain=False)
    video_audio = os.path.join(
        __root, "file", "generator", video_name + ".wav")

    spectrum = fake_analyzer.analyze_audio_list(video_audio)

    # 獲取不會觸發trigger的聲音平均強度
    hz_avg_strength_list = list()
    avg_strength = float()
    for time in spectrum:
        hz_avg_strength_list.append(
            _segment_strength(time[1], vocal_frequency_range))
    hz_avg_strength_list.sort()
    thirty_percent = int(len(hz_avg_strength_list)*trigger)
    avg_strength = sum(
        hz_avg_strength_list[0:thirty_percent]) / float(thirty_percent)

    # 區分高於平均與否的segments
    above_avg = list()
    below_avg = list()
    for time in spectrum:
        if _segment_strength(time[1], vocal_frequency_range) >= avg_strength:
            above_avg.append(time[0])
        else:
            below_avg.append(time[0])

    segments_list = _tiny_segments_concat(
        above_avg) + _tiny_segments_concat(below_avg)
    segments_list.sort(key=lambda foo: foo[0])

    log.i('sements_list is: {}'.format(segments_list))
    return segments_list


def _segment_strength(segment, vocal_frequency_range):
    vocal_hz_strength = list()
    for hz_strength in segment:
        if hz_strength[0] > vocal_frequency_range[0]:
            vocal_hz_strength.append(hz_strength[1])
            if not hz_strength[0] < vocal_frequency_range[1]:
                vocal_hz_strength.pop()
                return sum(vocal_hz_strength) / float(len(vocal_hz_strength))


def _tiny_segments_concat(segments: list):
    if len(segments) == 0:
        return []

    concated_segments = list()

    segments.reverse()
    start_time, end_time = segments.pop()
    segments.reverse()
    segments.append((-1.0, -1.0))  # 終止信號

    for segment in segments:
        if segment[0] == end_time:
            end_time = segment[1]
        else:
            concated_segments.append((start_time, end_time))
            start_time, end_time = segment
    return concated_segments
