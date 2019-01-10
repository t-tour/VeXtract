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

from scipy.io import wavfile
import numpy as np

from pathlib import Path
from wave import Wave_read
import wave

from generator.video import video_process as vp

AUDIO_STORAGE_LOCATION = os.path.join(__root, "file", "audio_storage_path")


class Audio():

    wave: Wave_read

    def __init__(self, path: Path):
        path_extinction_name = path.suffixes[-1]
        if path_extinction_name.endswith("wav"):
            self.path = path
        else:
            video_path_str = path.as_posix()  # 原先的path並非 pathlib的Path 而是能表示位置的string
            audio_path_str = AUDIO_STORAGE_LOCATION
            self.path = Path(AUDIO_STORAGE_LOCATION, path.stem + ".wav")
            vp.video_encoding(video_path_str, audio_path_str, self.path.name)
        wave_file_str = self.path.as_posix()
        _, self.bits = wavfile.read(wave_file_str)
        self.wave = wave.open(wave_file_str, 'rb')
