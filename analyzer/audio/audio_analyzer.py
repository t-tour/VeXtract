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
import random

import numpy as np
from scipy import signal
from scipy.io import wavfile

from analyzer.audio.frame import AudioAnalyzerFrame
from analyzer.audio.audio import Audio


class AudioAnalyzer():

    def __init__(self, audio: Audio, frame_time_less_equal_to=0.1, frame_frequency_less_equal_to=25.0, vocal_interval=(125, 450)):
        self.audio = audio
        self.position = -1
        self.vocal_interval = vocal_interval
        self.set_frame_frequencyless_equal_to(frame_frequency_less_equal_to)
        self.set_frame_time_less_equal_to(frame_time_less_equal_to)

    def set_frame_time_less_equal_to(self, interval: float):
        self.frame_time_smaller_then = interval
        frame_rate = self.audio.wave.getframerate()
        frame_bitsize_compute_maximum = frame_rate * self.frame_time_smaller_then
        power = math.ceil(math.log2(frame_bitsize_compute_maximum))
        self._frame_bitsize_maximum = int(math.pow(2, power))

    def set_frame_frequencyless_equal_to(self, interval: float):
        self.frame_frequency_less_equal_to = interval
        frame_rate = self.audio.wave.getframerate()
        frame_bitsize_compute_miniment = frame_rate / self.frame_frequency_less_equal_to
        power = math.ceil(math.log2(frame_bitsize_compute_miniment))
        self._frame_bitsize_minimum = int(math.pow(2, power))

    def get_overlap(self):
        try:
            maximum = self._frame_bitsize_maximum
            minimum = self._frame_bitsize_minimum
        except AttributeError:
            return  # 判斷是否參數設定完成
        if (maximum - minimum) < 0:
            return abs(maximum - minimum)
        else:
            return 0

    def get_frame_bitsize(self):
        return self._frame_bitsize_minimum

    def get_avg_strength_by_estimate(self) -> float:
        total = 0
        for _ in range(10000):
            frame = self.get_frame(random.randint(0, self.count_frame() - 1))
            total += frame.get_frequency_strength()
        return total / 10000

    def get_frame(self, index: int) -> AudioAnalyzerFrame:
        if index >= self.count_frame():
            raise IndexError

        bit_rate = self.audio.wave.getframerate()
        bits_size = self.get_frame_bitsize()
        start_bit_at = bits_size * index
        start_time_at = start_bit_at / bit_rate
        end_bit_at = start_bit_at + bits_size + self.get_overlap()
        end_bit_at = end_bit_at if end_bit_at <= self.audio.wave.getnframes(
        ) else self.audio.wave.getnframes()
        end_time_at = end_bit_at / bit_rate
        target_frame_bits = self.audio.bits[start_bit_at:end_bit_at]
        return AudioAnalyzerFrame((start_time_at, end_time_at), bit_rate, self.vocal_interval, target_frame_bits)

    def count_frame(self) -> int:
        bit_count = self.audio.wave.getnframes()
        frame_size = self.get_frame_bitsize()
        overlap = self.get_overlap()
        frame_count = math.ceil(bit_count / (frame_size - overlap))
        return frame_count

    def __iter__(self):
        return self

    def __next__(self) -> AudioAnalyzerFrame:
        if self.position == self.count_frame() - 1:
            raise StopIteration
        self.position += 1
        return self.get_frame(self.position)
