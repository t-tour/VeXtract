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

from analyzer.audio.audio import Audio

AUDIO_PATH = Path(os.path.join(__root, "test", "test_file", "test_video.mp4"))


def test_create_Audio():
    audio = Audio(Path(AUDIO_PATH))

    print()
