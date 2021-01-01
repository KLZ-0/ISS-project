import sys
from os import path
from pathlib import Path

from iss.audioproc import AudioProcessor

PYTHON_MIN_VERSION = (3, 5)


def setup_environment():
    rv = sys.version_info

    if not rv >= PYTHON_MIN_VERSION:
        print("Minimal required Python version is 3.5"
              f"\nYou are running {sys.version_info.major}.{sys.version_info.minor}", file=sys.stderr)
        sys.exit(1)

    Path("outputs").mkdir(parents=True, exist_ok=True)


def process_all():
    proc = AudioProcessor()
    proc.process_signals()

    print("Outputs generated to: " + path.abspath("outputs"))
