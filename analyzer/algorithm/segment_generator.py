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

import math

from generator.video import video_process
from analyzer.audio import dvpt_audio_analyze


MINIMUM_LENGTH = 2000
VOCAL_FREQUENCY_REANGE = (125, 400)
TRIGGER = 0.3
TRIGGER_MULTIPLE = 2


def generate_segments(video_or_audio, minimum_length=MINIMUM_LENGTH, vocal_frequency_range=VOCAL_FREQUENCY_REANGE, percentage=TRIGGER, trigger_multiple=TRIGGER_MULTIPLE, stability="Not Use Now"):
    """
    video:影片
    minimum_length:最小長度 milisecond
    vocal_frequency_range:人聲判定範圍
    trigger:無人聲準位
    trigger_times:觸發的平均倍數水準
    stability:防止彈跳
    """
    log.i('Start generate_segments with {}'.format(video_or_audio))

    # video轉聲訊
    file_name, file_extension = file_path_transfer(video_or_audio)
    if file_extension != "wav":
        video_process.video_encoding(video_or_audio, os.path.join(
            __root, "file", "generator"), file_name + ".wav", ifMain=False)
        video_audio_path = os.path.join(
            __root, "file", "generator", file_name + ".wav")
    else:
        video_audio_path = video_or_audio

    spectrums = dvpt_audio_analyze.analyze_audio_list(
        video_audio_path, frame_size=48000)

    avg_strength = _avg_segments_strength(
        spectrums, vocal_frequency_range, percentage)

    # 區分高於平均與否的segments
    above_avg = list()
    below_avg = list()
    for spectrum in spectrums:
        if _segment_strength(spectrum["spectrum"], vocal_frequency_range) >= avg_strength * trigger_multiple:
            above_avg.append(spectrum["time"])
        else:
            below_avg.append(spectrum["time"])

    segments_list = _segments_concat(
        above_avg) + _segments_concat(below_avg)
    segments_list.sort(key=lambda foo: foo[0])

    # segments過短合併
    minimum_concated_segments_list = _segments_list_minimum_base_concat(
        segments_list, minimum_length)
    return minimum_concated_segments_list


def file_path_transfer(file_path):
    file_path_list = file_path.split(os.sep)
    full_file_name = file_path_list[-1]
    file_name = ".".join(full_file_name.split(".")[0:-1])
    file_extension = full_file_name.split(".")[-1]
    return file_name, file_extension


def _segments_list_minimum_base_concat(origin_segments_list, minimum_length):
    selected_segments_list = list()
    new_segments_list = list()
    for selected_segment, i in zip(origin_segments_list, range(len(origin_segments_list))):
        selected_segments_list.append(selected_segment)
        selected_segment = _segments_concat(selected_segments_list)[0]
        if (selected_segment[1] - selected_segment[0]) * 1000 < minimum_length:
            if i == len(origin_segments_list) - 1:
                back_one = new_segments_list.pop()
                new_segments_list.append(
                    _segments_concat([back_one, selected_segment]).pop())
            continue
        else:
            selected_segments_list = list()
            new_segments_list.append(selected_segment)
    return new_segments_list


def _avg_segments_strength(spectrums, vocal_frequency_range, percentage):
    hz_strength_list = list()
    for spectrum in spectrums:
        hz_strength_list.append(
            _segment_strength(spectrum["spectrum"], vocal_frequency_range))
    hz_strength_list.sort()
    thirty_percent = int(len(hz_strength_list) * percentage)
    avg_strength = sum(
        hz_strength_list[0:thirty_percent]) / float(thirty_percent)
    log.i('Avg_strength: {}'.format(avg_strength))
    return avg_strength


def _segment_strength(segment, appoint_vocal_frequency_range):
    segment_frequency_interval = segment[1][0]
    segment_frequency_limitation = segment[len(segment) - 1][0]
    if appoint_vocal_frequency_range[0] < 0:
        raise Exception("appoint_vocal_frequency_range out of bound.")
    if appoint_vocal_frequency_range[1] > segment_frequency_limitation:
        raise Exception("appoint_vocal_frequency_range out of bound.")
    slice_segment_start_section = appoint_vocal_frequency_range[0] / \
        segment_frequency_interval
    slice_segment_end_section = appoint_vocal_frequency_range[1] / \
        segment_frequency_interval
    strength_list = list()
    for appoint_frequency in segment[math.ceil(slice_segment_start_section):math.ceil(slice_segment_end_section)]:
        strength_list.append(abs(appoint_frequency[1]))
    return sum(strength_list)


def _segments_concat(segments: list):
    if len(segments) == 0:
        return []
    elif len(segments) == 1:
        return segments

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
    segments = concated_segments
    return concated_segments
