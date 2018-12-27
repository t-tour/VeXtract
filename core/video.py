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

from typing import List, Tuple
from pathlib import Path
import math

from core.audio import Audio
from core.scene.factory import GeneratorFactory
from core.common.audio_analyzer import AudioAnalyzer
from core.common.segment import Segment
from core.scene.scene import Scene
from core.common.evaluation_resources import EvaluationResources
from generator.video import video_process

_ROOT = __root


class Video(object):

    segments: List[Segment]
    scenes: List[Scene]

    def __init__(self, path: Path):
        self.row_video_path = path
        self.audio = Audio(path)
        self.segments = list()
        self.scenes = list()

    def generate_scenes(self, method='static'):
        self._generate_segments()
        generator = GeneratorFactory.product(self, method)
        self.scenes = generator.generate_scenes()
        

    def _generate_segments(self):
        analyzer = AudioAnalyzer(self.audio)
        avg_strength = analyzer.get_avg_strength_by_estimate()
        for audio_frame in analyzer:
            frame_strength = audio_frame.get_frequency_strength()
            isvocal = frame_strength > avg_strength
            self.segments.append(audio_frame.frame2segment(isvocal))

    def set_evaluation_resources(self, er: EvaluationResources):
        self.evaluation_resources = er

    def evaluate(self):
        er = self.evaluation_resources
        interval = self.segments[0].get_interval()

        if er.is_real_time_comment_exist():
            for comment in er.get_real_time_comments():
                index_of_segment = math.floor(comment.get_timeat() / interval)
                try:
                    self.segments[index_of_segment].add_score(
                        3)  # 暫時措施 所有文字分數皆為3分
                except IndexError:
                    print('評分資料與影片 時長不一致')
                    log.e('評分資料與影片 時長不一致')
                    break

    def extract(self, method="greedy", length=60):
        """這是用來切分video用的，method表示使用的演算法"""
        if len(self.scenes) == 0:
            raise Exception("extract before generate scenes")

        cut_list = list()
        cut_list: List[Scene]

        if method == "greedy":
            scenes = sorted(
                self.scenes, key=lambda foo: foo.get_avg_score(), reverse=True)
            amount = 0
            for scene in scenes:
                amount += scene.get_interval()
                if amount < length:
                    cut_list.append(scene)

        else:
            raise Exception("unknow method")
        # TODO: lambda linting
        cut_list = sorted(cut_list, key=lambda foo: foo.get_startat())
        segments = [scene.get_time() for scene in cut_list]

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
        time_tags = concated_segments

        # TODO: 舊版func使用單純的path路徑
        path_str = self.row_video_path.as_posix()
        # TODO: 舊版func使用單純的time標籤
        self.new_path = Path(_ROOT, "file", "new_video_storage_path",
                             self.row_video_path.stem + " 10min" + self.row_video_path.suffix)
        # TODO: 舊版的func使用名稱與路徑分開
        location = self.new_path.parent.as_posix()
        filename = self.new_path.name

        video_process.video_process(
            path_str, time_tags, output_location=location, output_name=filename)
