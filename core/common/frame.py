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

import numpy as np
from numpy.fft import fft
from scipy import signal

from core.common.segment import Segment


class AudioAnalyzerFrame():

    def __init__(self, time: tuple, bitrate: int, vocal_interval: tuple, bits_data):
        self.time = time
        self.bitrate = bitrate
        self.vocal_interval = vocal_interval
        self.set_bits_data(bits_data)
        self._generate_spectrum()

    def set_bits_data(self, bits_data):
        shape = len(bits_data.shape)
        if shape == 2:
            self.bits_data = np.average(bits_data, 1)
        elif shape > 2:
            raise Exception('unSupport nchannel')
        else:
            self.bits_data = bits_data

    def _generate_spectrum(self):
        self.frequency, _, spectrum_rawvalue = signal.stft(
            self.bits_data, self.bitrate, nperseg=self.bits_data.shape[0], noverlap=0)
        self.spectrum = np.average(spectrum_rawvalue, 1)

    def get_frequency_strength(self) -> float:
        frequency_interval = self.frequency[1]
        startat = math.ceil(self.vocal_interval[0] / frequency_interval)
        endat = math.ceil(self.vocal_interval[1] / frequency_interval)

        total = 0
        for index in range(startat, endat):
            total += abs(self.spectrum[index])
        return total / (endat - startat)

    def get_interval(self):
        return self.time[1] - self.time[0]

    def frame2segment(self, isvocal):
        return Segment(self.time, isvocal)
