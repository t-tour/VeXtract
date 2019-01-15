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
from typing import List, Tuple
import re
import subprocess

import ffmpeg

from core.scene.scene import Scene


class Ffmpeg_process():

    # TODO: google建議的vp9編碼參數詳見: https://developers.google.com/media/vp9/settings/vod/
    def __init__(self, input_media_path: Path, output_media_path: Path):
        self.CONFIG_720P = {'b:v': '1800k', 'minrate': '900k', 'maxrate': '2610k', 'tile-columns': '2', 'g': '240',
                            'threads': '8', 'quality': 'good', 'crf': '32', 'c:v': 'libvpx-vp9', 'c:a': 'libopus', 'speed': '4'}
        self.SCRIPT_TEMP_PATH = Path(
            _ROOT, "file", "temp", "ffmpeg_filtergraph.txt")
        self.input_media_path = input_media_path
        self.output_media_path = output_media_path

    def type_change(self, type):
        # TODO: Implement Request.
        raise NotImplementedError

    def get_duration(self):
        # TODO: Implement Request.
        raise NotImplementedError

    @log.logit
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
        stream = ffmpeg.output(
            v_stream, a_stream, outputfile, **self.CONFIG_720P)
        # ffmpeg.view(stream)  # Debug
        self.stream = stream
        return ' '.join(ffmpeg.compile(stream))

    def _estublish_filterscript(self, cmd) -> Tuple[str, Path]:
        groups = re.match(
            r'ffmpeg -i (?P<input>.*) -filter_complex (?P<filter_complex>.*?) (?P<maps>-.*]) (?P<output>.*)', cmd)
        new_cmd = "ffmpeg -i {input_path} -filter_complex_script {script} {maps} {output_path}".format(
            input_path=groups["input"], output_path=groups["output"], maps=groups["maps"], script=self.SCRIPT_TEMP_PATH.as_posix())
        with self.SCRIPT_TEMP_PATH.open('w', encoding='utf-8') as f:
            f.write(groups["filter_complex"])
        return new_cmd, self.SCRIPT_TEMP_PATH

    @log.logit
    def cut(self, scenes: List[Scene]):
        cmd = self._estublish_cmd(scenes)
        scripted_cmd, _ = self._estublish_filterscript(cmd)
        subprocess.run(scripted_cmd, check=True, encoding='utf-8')
        self.SCRIPT_TEMP_PATH.unlink()
