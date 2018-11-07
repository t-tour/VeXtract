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

from analyzer.algorithm import segment_generator
from analyzer.algorithm import video_algorithm
from analyzer.audio import dvpt_audio_analyze
from generator.video import video_process

VIDEO = os.path.join(__root, "test", "test_file", "av23315808.mp4")
VIDEO_AUDIO = os.path.join(
    __root, "test", "test_file", "Ns_interval_vocal_with_noise.wav")
SEGMENTS = dvpt_audio_analyze.analyze_audio_list(VIDEO_AUDIO)


def test_generate_segments():
    log.i('Strat test_generate_segments.')
    a = segment_generator.generate_segments(VIDEO_AUDIO)
    assert_total_length = video_algorithm.get_video_length(VIDEO_AUDIO)
    total_length = 0
    for time in a:
        log.d("total={:.4f} start:{:.4f} end:{:.4f}".format(
            total_length, time[0], time[1]))
        total_length += time[1] - time[0]

    assert assert_total_length >= total_length
    assert assert_total_length - 0.5 <= total_length


def test__segment_strength():
    log.i('Start test__segment_strength')
    strength = segment_generator._segment_strength(
        SEGMENTS[0]['spectrum'], (0, 1))
    assert strength == abs(
        SEGMENTS[0]['spectrum'][0][1])


def test__segments_concat():
    test_segments = [(0.5, 2.5), (2.5, 3.7), (4.8, 5.9),
                     (7.6, 8.4), (8.4, 9.6)]
    concated_segments = segment_generator._segments_concat(test_segments)
    assert [(0.5, 3.7), (4.8, 5.9), (7.6, 9.6)] == concated_segments
