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
_ROOT = __root

from helper import logger
log = logger.Logger(__name__)

from core.scene.generator import Generator
from core.scene.generators import GeneratorVAD, GeneratorComment, GeneratorStatic
from core.common.evaluation_resources import EvaluationResources


class GeneratorFactory():

    @staticmethod
    def product(video, method) -> Generator:
        if method == 'VAD':
            return GeneratorVAD(video.segments)
        elif method == 'comment':
            return GeneratorComment(video.segments, video.evaluation_resources)
        elif method == 'static':
            return GeneratorStatic(video.segments)
        else:
            raise Exception("no such method.")
