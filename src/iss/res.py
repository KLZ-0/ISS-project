import sys
from os import path

audiopath = path.join(path.dirname(path.dirname(path.dirname(__file__))), "audio")
if not path.isdir(audiopath):
    print("The directory '" + path.abspath(audiopath) + "' does not exist", file=sys.stderr)
    sys.exit(1)

# 20ms frames @ 16kHz
# because of 15 -> 25
# in s
SAMPLE_DURATION = 1
FRAME_DURATION = 0.025
ALIGNED_FRAME_DURATION = 0.020

CORREL_FREQ_MARGIN = 500

FIG_SIZE = (10, 2.5)

# task 15
ALIGN_MIN_FREQ = 100
