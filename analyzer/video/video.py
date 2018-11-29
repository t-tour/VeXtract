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

from analyzer.audio.audio import Audio
from analyzer.audio.audio_analyzer import AudioAnalyzer
from analyzer.evaluation_resources import EvaluationResources

class Video(object):

    def __init__(self, path):
        self.MINIMUM_LENGTH = 2000
        self.VOCAL_FREQUENCY_REANGE = (125, 400)
        self.TRIGGER = 0.5
        self.TRIGGER_MULTIPLE = 2
        self.audio = Audio(path)
        self.vocal_segments = list()
        self.nonvocal_segments = list()

    def generate_split_segments(self):
        analyzer = AudioAnalyzer(self.audio, vocal_interval=self.VOCAL_FREQUENCY_REANGE)
        avg_strength = analyzer.get_avg_strength_by_estimate()
        for audio_frame in analyzer:
            frame_strength = audio_frame.get_frequency_strength()
            if frame_strength > avg_strength:
                self.vocal_segments.append(audio_frame.frame2segment())
            else:
                self.nonvocal_segments.append(audio_frame.frame2segment())

    def set_evaluation_resources(self, er: EvaluationResources):
        # TODO: Implement Request.
        raise Exception("Not Implment yet!")

    def evaluate(self):
        # TODO: Implement Request.
        raise Exception("Not Implment yet!")

    def extract(self):
        # TODO: Implement Request.
        raise Exception("Not Implment yet!")
