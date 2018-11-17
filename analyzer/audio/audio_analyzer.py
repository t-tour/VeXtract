import os
import sys
__root = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__)) + (os.sep + '..') * (
        len(os.path.dirname(os.path.abspath(__file__)).split(os.sep))
        - os.path.dirname(os.path.abspath(__file__)).split(os.sep).index(
            'VeXtract'
        ) - 1
    )) + os.sep
sys.path.append(__root)

from helper import logger
log = logger.Logger(__name__)

from pathlib import Path
import wave

import numpy as np

from analyzer.audio.spectrum import Spectrum

class AudioAnalyzer():

    def __init__(self, path: Path):
        self.path = path
        pure_path = path.as_posix()
        self.wave_file = wave.open(pure_path, 'rb')
        self.position = int()

    def set_spectrum_time_minimum(self, interval: float):
        self.spectrum_time_minimum = float()
        pass

    def set_spectrum_frequency_minimum(self, interval: float):
        self.spectrum_frequency_minimum = float()
        pass

    def next_spectrum(self) -> Spectrum:
        pass

    def count_spectrum(self):
        pass

    def set_position(self):
        pass

    def __iter__(self):
        pass

    