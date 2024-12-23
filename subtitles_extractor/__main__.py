import os
import time
from pathlib import Path

from subtitles_extractor import ffmpeg
from subtitles_extractor.cache import File, get_hash, read_cache, write_cache


def run(
    libraries: list[str],
    sleep: int,
    forced: bool,
    skip_srt: bool,
    strip_formatting: bool,
    langs: list[str],
    data_dir: Path,
    forced_title: list[str],
):
    cache_file = data_dir / "filelist.cache"
    p_hash = get_hash(forced, skip_srt, strip_formatting, langs, forced_title)
    cache = read_cache(cache_file, p_hash)

    while True:
        files = set()
        for lib in libraries:
            lib_path = Path(lib)
            for path in lib_path.rglob("*"):
                if (
                    path.is_file()
                    and (time.time() - path.stat().st_mtime) > 300
                ):
                    files.add(File(path))

        for file in sorted(files - cache):
            ffmpeg.save_subtitles(
                file.name,
                forced,
                skip_srt,
                strip_formatting,
                langs,
                forced_title,
            )

        if cache != files:
            cache = files
            write_cache(cache_file, p_hash, cache)

        time.sleep(sleep * 60)


def main():
    libraries = os.environ.get("SUBTITLES_EXTRACTOR_LIBRARIES", "").split(";")
    sleep = int(os.environ.get("SUBTITLES_EXTRACTOR_SLEEP", 1))
    forced = bool(int(os.environ.get("SUBTITLES_EXTRACTOR_FORCED_ONLY", 1)))
    skip_srt = bool(int(os.environ.get("SUBTITLES_EXTRACTOR_SKIP_SRT", 1)))
    strip_formatting = bool(
        int(os.environ.get("SUBTITLES_EXTRACTOR_STRIP_FORMATTING", 1))
    )
    langs = os.environ.get("SUBTITLES_EXTRACTOR_LANGUAGES", "*").split(";")
    data_dir = Path(os.environ.get("SUBTITLES_EXTRACTOR_DATA_DIR", "."))
    forced_title = os.environ.get(
        "SUBTITLES_EXTRACTOR_FORCED_TITLE", ""
    ).split(";")

    try:
        run(
            libraries,
            sleep,
            forced,
            skip_srt,
            strip_formatting,
            langs,
            data_dir,
            forced_title,
        )
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
