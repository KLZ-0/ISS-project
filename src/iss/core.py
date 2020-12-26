from iss.audioproc import AudioProcessor

import sys

from pathlib import Path

PYTHON_MIN_VERSION = (3, 5)


def setup_environment():
    rv = sys.version_info

    # TODO: Probably make this version independent
    if not rv >= PYTHON_MIN_VERSION:
        print("Minimal required Python version is 3.5"
              f"\nYou are running {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)

    Path("outputs").mkdir(parents=True, exist_ok=True)


def process_all():
    proc = AudioProcessor()
