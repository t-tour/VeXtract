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
_ROOT = __root

from helper import logger
log = logger.Logger(__name__)

from pathlib import Path
from typing import List

import ffmpeg

from core.common.scene import Scene


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class TransitionError(Error):
    """Raised when an operation attempts a state transition that's not
    allowed.

    Attributes:
        previous -- state at beginning of transition
        next -- attempted new state
        message -- explanation of why the specific transition is not allowed
    """

    def __init__(self, previous, next, message):
        self.previous = previous
        self.next = next
        self.message = message


class Ffmpeg_process():

    def __init__(self, input_media_path: Path, output_media_path: Path):
        self.TEMP_PATH = Path(_ROOT, "file", "temp")
        self.input_media_path = input_media_path
        self.output_media_path = output_media_path

    def type_change(self, type):
        # TODO: Implement Request.
        raise NotImplementedError

    def get_duration(self):
        # TODO: Implement Request.
        raise NotImplementedError

    def _estublish_cmd(self, scenes: List[Scene]):
        inputfile = self.input_media_path.as_posix()
        outputfile = self.output_media_path.as_posix()
        stream = ffmpeg.input(inputfile)
        video_streams = list()
        audio_streams = list()
        for scene in scenes:
            start = scene.get_startat()
            duration = scene.get_interval()
            v_clip_stream = ffmpeg.trim(
                stream, start=start, duration=duration)
            v_clip_stream = ffmpeg.setpts(v_clip_stream, 'PTS-STARTPTS')
            a_clip_stream = ffmpeg.filter_(
                stream, 'atrim', start=start, duration=duration)
            a_clip_stream = ffmpeg.filter_(
                a_clip_stream, 'asetpts', 'PTS-STARTPTS')

            video_streams.append(v_clip_stream)
            audio_streams.append(a_clip_stream)
        v_stream = ffmpeg.concat(
            *video_streams, n=len(video_streams), v=1, a=0)
        a_stream = ffmpeg.concat(
            *audio_streams, n=len(audio_streams), v=0, a=1)
        stream = ffmpeg.output(v_stream, a_stream, outputfile)
        # ffmpeg.view(stream)  # Debug
        self.stream = stream
        return ' '.join(ffmpeg.compile(stream))

    def cut(self, scenes: List[Scene]):
        self._estublish_cmd(scenes)
        ffmpeg.run(self.stream)
