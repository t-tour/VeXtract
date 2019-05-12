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
import tempfile

import ffmpeg
import numpy as np
import cv2
import tensorflow as tf


from generator.video import video_process
from core.audio import Audio
from core.scene.factory import GeneratorFactory
from core.common.audio_analyzer import AudioAnalyzer
from core.common.segment import Segment
from core.scene.scene import Scene
from core.common.evaluation_resources import EvaluationResources
from core.ffmepg_processor import Ffmpeg_process

_ROOT = __root
VIDEO_STORAGE_LOCATION = Path(_ROOT, "file", "extracted_video_storage_path")


class Video(object):
    """Video 整個執行環境的主體，new出來需要有影片路徑\n
    剪出來的影片之後會儲存在 VIDEO_STORAGE_LOCATION\n
    路徑上\n
    example:
    ```
    from core.common.evaluation_resources import EvaluationResources

    v = Video("c.mp4")
    er = EvaluationResources(Crawler的資料)
    v.set_evaluation_resources(er)
    v.generate_segments()
    v.generate_scenes()
    v.evaluate()
    v.select_scenes()
    v.extract()
    ```
    """

    segments: List[Segment]
    scenes: List[Scene]
    selected_scenes_list: List[Scene]

    def __init__(self, path: Path):
        if not path.is_file():
            raise Exception("path not found")
        self.row_video_path = path
        self.segments = list()
        self.scenes = list()
        self.evaluation_resources = None

    @log.logit
    def generate_scenes(self, method='static'):
        if not self.segments:
            raise Exception("generate_scenes before generate_segment")
        self.generator = GeneratorFactory.product(self, method)
        self.scenes = self.generator.generate_scenes()

    @log.logit
    def generate_segments(self):
        duration = Ffmpeg_process.get_duration(self.row_video_path)
        for second in range(int(duration)):
            self.segments.append(Segment((second, second + 1)))

    def set_evaluation_resources(self, er: EvaluationResources):
        self.evaluation_resources = er

    @log.logit
    def evaluate(self):
        # Scene 裡面每個seg都是1S  在stataic 情況下
        interval = self.segments[0].get_interval()

        if not self.evaluation_resources:
            cap = cv2.VideoCapture(self.row_video_path.as_posix())

            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            need_frames = int(total_frames * 4 / fps)

            data = np.asarray(
                [cv2.resize(cap.read(int(n * fps / 4))[1], (128, 72)) for n in range(need_frames)])
            data = np.resize(data, (int(need_frames / 20) * 20, 72, 128, 3))
            data = np.reshape(data, (int(need_frames / 20), 20, 72, 128, 3))
            model = tf.contrib.keras.models.load_model(
                os.path.join(_ROOT, 'models/model2_100ep.h5'))
            prdicted_data = model.predict(data, batch_size=1, verbose=0)
            for index, score in enumerate(prdicted_data):
                for segment in self.scenes[index].segments:
                    segment.score = score
        else:
            for comment in self.evaluation_resources.get_real_time_comments():
                index_of_segment = math.floor(comment.get_timeat_second() / interval)
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
        self.new_path = Path(VIDEO_STORAGE_LOCATION, filename)

    @log.logit
    def extract(self):
        if not self.selected_scenes_list:
            raise Exception("extract before select_scenes")
        os.makedirs(self.new_path.parent, exist_ok=True)
        fp = Ffmpeg_process(self.row_video_path, self.new_path)
        fp.cut(self.selected_scenes_list)
