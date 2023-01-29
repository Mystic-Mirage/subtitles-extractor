import os
import time
from pathlib import Path

from subtitles_extractor import ffmpeg


def run(libraries, sleep, forced, langs):
    while True:
        for lib in libraries:
            lib_path = Path(lib)
            for path in lib_path.rglob("*"):
                if path.is_file():
                    ffmpeg.save_subtitles(str(path), forced, langs)
        time.sleep(sleep * 60)


def main():
    libraries = os.environ.get("SUBTITLES_EXTRACTOR_LIBRARIES", "").split(";")
    sleep = int(os.environ.get("SUBTITLES_EXTRACTOR_SLEEP", 1))
    forced = bool(int(os.environ.get("SUBTITLES_EXTRACTOR_FORCED_ONLY", 1)))
    langs = os.environ.get("SUBTITLES_EXTRACTOR_LANGUAGES", "*").split(";")

    try:
        run(libraries, sleep, forced, langs)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
