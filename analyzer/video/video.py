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

from typing import List
import math

from analyzer.audio.audio import Audio
from analyzer.audio.audio_analyzer import AudioAnalyzer
from analyzer.segment import Segment
from analyzer.scene import Scene
from analyzer.evaluation_resources import EvaluationResources


class Video(object):

    segments: List[Segment]
    scenes: List[Scene]

    def __init__(self, path, scene_minimum_length=2, scene_maximum_length=60):
        self.scene_minimum_length = scene_minimum_length
        self.scene_maximum_length = scene_maximum_length
        self.VOCAL_FREQUENCY_REANGE = (125, 400)
        self.audio = Audio(path)
        self.segments = list()
        self.scenes = list()

    def generate_segments(self):
        analyzer = AudioAnalyzer(
            self.audio, vocal_interval=self.VOCAL_FREQUENCY_REANGE)
        avg_strength = analyzer.get_avg_strength_by_estimate()
        for audio_frame in analyzer:
            frame_strength = audio_frame.get_frequency_strength()
            isvocal = frame_strength > avg_strength
            self.segments.append(audio_frame.frame2segment(isvocal))

    def generate_split_scenes(self):
        # FIXME: 最後一個scene太短收不到
        empty_scene = Scene(self.scene_minimum_length,
                            self.scene_maximum_length)
        scene = empty_scene.copy()
        for segment in self.segments:
            if scene.istooshort():
                scene.add_segment(segment)
            elif scene.istoolong():
                self.scenes.append(scene)
                scene = empty_scene.copy()
                scene.add_segment(segment)
            else:
                if segment.isvocal == scene.is_accept_vocal():
                    scene.add_segment(segment)
                else:
                    self.scenes.append(scene)
                    scene = empty_scene.copy()
                    scene.add_segment(segment)
        if scene.istooshort():
            for segment in scene.segments:
                self.scenes[-1].add_segment(segment)
        elif scene != self.scenes[-1]:
            self.scenes.append(scene)

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

    def extract(self):
        # TODO: Implement Request.
        raise Exception("Not Implment yet!")
