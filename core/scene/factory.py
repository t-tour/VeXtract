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

from core.scene.generator import Generator
from core.scene.generators import GeneratorVAD, GeneratorComment, GeneratorStatic
from core.video import Video


class GeneratorFactory():

    @staticmethod
    def product(video: Video, method) -> Generator:
        if method == 'VAD':
            return GeneratorVAD(video.segments)
        elif method == 'comment':
            return GeneratorComment()
        elif method == 'static':
            return GeneratorStatic()
        else:
            raise Exception("no such method.")
