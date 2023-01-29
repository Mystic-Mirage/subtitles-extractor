import os
import subprocess
import sys

from subtitles_extractor import EXT, ffprobe


def save_subtitles(filename: str, forced=False, langs=None):
    langs = langs or ["*"]
    ext_exclude = tuple(os.extsep + ext for ext in (EXT, "nfo", "txt"))
    if filename.endswith(ext_exclude) or "-TdarrCacheFile-" in filename:
        return

    subtitles = ffprobe.subtitles(filename)
    if subtitles is None:
        return

    for idx, data in subtitles.items():
        dst = ffprobe.subtitles_path(filename, data)

        if not (
            (data["codec"] != "subrip" and not data["bitmap"])
            and (forced and data["forced"] or not forced)
            and ("*" in langs or data["language"] in langs)
        ):
            try:
                dst.unlink()
            except FileNotFoundError:
                pass
            else:
                print(f"Unlinked: {dst}")
            continue

        proc = subprocess.run(
            [
                "ffmpeg",
                "-v",
                "error",
                "-y",
                "-i",
                filename,
                "-map",
                f"0:{idx}",
                str(dst),
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if proc.returncode != 0:
            print(
                f"FFMPEG error: {filename}: " + proc.stderr.decode(),
                file=sys.stderr,
            )
        elif dst.exists():
            print(f"Extracted: {dst}")


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        save_subtitles(filename)
