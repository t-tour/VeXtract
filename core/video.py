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
from core.common.audio_analyzer import AudioAnalyzer
from core.common.segment import Segment
from core.common.scene import Scene
from core.common.evaluation_resources import EvaluationResources
from generator.video import video_process

_ROOT = __root


class Video(object):

    segments: List[Segment]
    scenes: List[Scene]

    def __init__(self, path: Path, scene_minimum_length=2, scene_maximum_length=60):
        self.row_video_path = path
        self.scene_minimum_length = scene_minimum_length
        self.scene_maximum_length = scene_maximum_length
        self.VOCAL_FREQUENCY_REANGE = (125, 400)
        self.audio = Audio(path)
        self.segments = list()
        self.scenes = list()

    def generate_scenes(self):
        self._generate_segments()
        self._generate_split_scenes()
        self._concat_scenes()

    def _generate_segments(self):
        analyzer = AudioAnalyzer(
            self.audio, vocal_interval=self.VOCAL_FREQUENCY_REANGE)
        avg_strength = analyzer.get_avg_strength_by_estimate()
        for audio_frame in analyzer:
            frame_strength = audio_frame.get_frequency_strength()
            isvocal = frame_strength > avg_strength
            self.segments.append(audio_frame.frame2segment(isvocal))

    def _generate_split_scenes(self):
        # TODO: 重構需求現階段先排除segment震盪問題，往後可能需要語者分析與更穩定的VAD方法
        empty_scene = Scene(self.scene_minimum_length,
                            self.scene_maximum_length)
        scene = empty_scene.copy()

        for segment in self.segments:
            if len(scene.segments) == 0:
                scene.add_segment(segment)
            segment_is_vocal = 1 if segment.isvocal else 0
            if scene.get_vocal_avg() == segment_is_vocal:
                scene.add_segment(segment)
            else:
                self.scenes.append(scene)
                scene = empty_scene.copy()
                scene.add_segment(segment)
        # add the last one scene
        self.scenes.append(scene)

    def _concat_scenes(self):
        new_scenes_list = list()
        compare_scenes_list = list()

        for add_scene in self.scenes:
            compare_scenes_list.append(add_scene)
            amount = 0
            for scene in compare_scenes_list:
                amount += scene.get_interval()
            if amount > scene.minimum_length:
                new_scenes_list.append(Scene.join_scenes(compare_scenes_list))
                compare_scenes_list = list()
            else:
                continue
        if len(compare_scenes_list) != 0:
            last_scene = new_scenes_list.pop()
            compare_scenes_list.insert(0, last_scene)
            new_last_scene = Scene.join_scenes(compare_scenes_list)
            new_scenes_list.append(new_last_scene)
        self.scenes = new_scenes_list

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

    def extract(self, method="basic", length = 60):
        if len(self.scenes) == 0:
            raise Exception("extract before generate scenes")

        cut_list = list()
        cut_list: List[Scene]

        if method == "basic":
            scenes = sorted(self.scenes, key=lambda foo: foo.get_avg_score())
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
