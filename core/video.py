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

from typing import List, Tuple
from pathlib import Path
import math


from generator.video import video_process
from core.audio import Audio
from core.scene.factory import GeneratorFactory
from core.common.audio_analyzer import AudioAnalyzer
from core.common.segment import Segment
from core.scene.scene import Scene
from core.common.evaluation_resources import EvaluationResources
from core.ffmepg_processor import Ffmpeg_process

_ROOT = __root


class Video(object):

    segments: List[Segment]
    scenes: List[Scene]
    selected_scenes_list: List[Scene]

    def __init__(self, path: Path):
        self.row_video_path = path
        self.audio = Audio(path)
        self.segments = list()
        self.scenes = list()

    @log.logit
    def generate_scenes(self, method='static'):
        if not self.segments:
            raise Exception("generate_scenes before generate_segment")
        self.generator = GeneratorFactory.product(self, method)
        self.scenes = self.generator.generate_scenes()

    @log.logit
    def generate_segments(self):
        analyzer = AudioAnalyzer(self.audio)
        avg_strength = analyzer.get_avg_strength_by_estimate()
        for audio_frame in analyzer:
            frame_strength = audio_frame.get_frequency_strength()
            isvocal = frame_strength > avg_strength
            self.segments.append(audio_frame.frame2segment(isvocal))

    def set_evaluation_resources(self, er: EvaluationResources):
        self.evaluation_resources = er

    @log.logit
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

    @log.logit
    def select_scenes(self, method='greedy', length=60):
        """這是用來選取scenes用的，method表示使用的演算法"""
        if len(self.scenes) == 0:
            raise Exception("select_scenes before generate scenes")

        selected_scenes_list = list()

        if method == "greedy":
            scenes = sorted(
                self.scenes, key=lambda foo: foo.get_avg_score(), reverse=True)
            amount = 0
            for scene in scenes:
                amount += scene.get_interval()
                if amount < length:
                    selected_scenes_list.append(scene)

        else:
            raise Exception("unknow method")
        # TODO: lambda linting
        self.selected_scenes_list = sorted(
            selected_scenes_list, key=lambda foo: foo.get_startat())

        filename = "{}-{}-{}-{}{}".format(self.row_video_path.stem, type(
            self.generator).__name__, method, length, ".webm")
        self.new_path = Path(_ROOT, "file", "new_video_storage_path", filename)

    # Not Need right now
    @log.logit
    def _concat_selected_scenes(self):
        if not self.selected_scenes_list:
            raise Exception("_concat_selected_scenes before select_scenes")

        front_scene = self.selected_scenes_list[0]

        for index, scene in enumerate(self.selected_scenes_list):
            if front_scene.isconected(scene):
                front_scene = scene
            else:
                # TODO: Implement Request.
                raise NotImplementedError

        # concated_cut_scenes_list = list()
        # end_scene = Scene()
        # end_scene.add_segment(Segment((-1, -1), False))

        # self.cut_scenes_list.reverse()
        # start_scene = self.cut_scenes_list.pop()
        # self.cut_scenes_list.reverse()
        # self.cut_scenes_list.append(end_scene)

        # temp_list_group = list()
        # for scene in self.cut_scenes_list:
        #     if start_scene.get_endat() == scene.get_startat():
        #         temp_list_group.append(scene)
        #     else:
        #         # TODO: Implement Request.
        #         raise NotImplementedError

        # segments = [scene.get_time() for scene in cut_scenes_list]

        # concated_segments = list()
        # segments.reverse()
        # start_time, end_time = segments.pop()
        # segments.reverse()
        # segments.append((-1.0, -1.0))  # 終止信號

        # for segment in segments:
        #     if segment[0] == end_time:
        #         end_time = segment[1]
        #     else:
        #         concated_segments.append((start_time, end_time))
        #         start_time, end_time = segment
        # time_tags = concated_segments

    @log.logit
    def extract(self):
        if not self.selected_scenes_list:
            raise Exception("extract before select_scenes")

        fp = Ffmpeg_process(self.row_video_path, self.new_path)
        fp.cut(self.selected_scenes_list)



        # time_tags = [scene.get_time() for scene in self.selected_scenes_list]
        # # TODO: 舊版func使用單純的path路徑
        # path_str = self.row_video_path.as_posix()
        # # TODO: 舊版func使用單純的time標籤
        # self.new_path = Path(_ROOT, "file", "new_video_storage_path",
        #                      self.row_video_path.stem + " 10min" + self.row_video_path.suffix)
        # # TODO: 舊版的func使用名稱與路徑分開
        # location = self.new_path.parent.as_posix()
        # location = location.replace("/", os.sep)
        # filename = self.new_path.name

        # video_process.video_process(
        #     path_str, time_tags, output_location=location, output_name=filename)