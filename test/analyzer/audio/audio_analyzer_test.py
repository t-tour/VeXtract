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

from pathlib import Path

from scipy.signal import stft
from scipy.io import wavfile
import numpy as np

from analyzer.audio.audio_analyzer import AudioAnalyzer
from analyzer.audio.audio import Audio

AUDIO_PATH = Path(__root, "test", "test_file",
                  "Ns_interval_vocal_with_noise.wav")
AUDIO_PATH_MONO = Path(__root, "test", "test_file", "mono.wav")
AUDIO = Audio(AUDIO_PATH_MONO)


def test_AudioAnalyzer():
    analyzer = AudioAnalyzer(AUDIO)
    frame_list = list()
    for frame in analyzer:
        a = frame.get_frequency_strength()
        print(frame)
    print()
