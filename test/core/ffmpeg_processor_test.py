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

from pathlib import Path
import hashlib

from core.ffmepg_processor import Ffmpeg_process
from core.common.scene import Scene
from core.common.segment import Segment

INPUT_PATH = Path(__root, "test", "test_file", "90s_video.mp4")
OUTPUT_PATH = Path(__root, "test", "test_file", "output.mp4")
fp = Ffmpeg_process(INPUT_PATH, OUTPUT_PATH)


SCENE1 = Scene(0, 0)
SCENE1.add_segment(Segment((20.0, 22.0), True))
SCENE2 = Scene(0, 0)
SCENE2.add_segment(Segment((25.0, 27.0), True))
SCENES_LIST = [SCENE1, SCENE2]


if OUTPUT_PATH.exists():
    raise Exception("輸出檔案存在")

HASH = "9aa2c5b199a2afc35fffe5d9bfe3072142434e0f483ec53b20947e6b6462bbae"
CMD = """\
ffmpeg -i {input_path} \
-filter_complex [0]trim=duration=2.0:start=20.0[s0];[s0]setpts=PTS-STARTPTS[s1];\
[0]trim=duration=2.0:start=25.0[s2];[s2]setpts=PTS-STARTPTS[s3];\
[s1][s3]concat=a=0:n=2:v=1[s4];\
[0]atrim=duration=2.0:start=20.0[s5];[s5]asetpts=PTS-STARTPTS[s6];\
[0]atrim=duration=2.0:start=25.0[s7];[s7]asetpts=PTS-STARTPTS[s8];\
[s6][s8]concat=a=1:n=2:v=0[s9] \
-map [s4] -map [s9] {output_path}\
""".format(input_path=INPUT_PATH.as_posix(), output_path=OUTPUT_PATH.as_posix())

def test_cut():
    fp.cut(SCENES_LIST)
    sha256 = hashlib.sha256()
    with fp.output_media_path.open(mode='rb') as f:
        sha256.update(f.read())
    assert sha256.hexdigest() == HASH
    OUTPUT_PATH.unlink()

def test_estublish_cmd():
    cmd = fp._estublish_cmd(SCENES_LIST)
    assert cmd == CMD