import os
import subprocess
import sys

from subtitles_extractor import EXT, ffprobe, formatting


def save_subtitles(
    filename: str,
    forced=False,
    skip_srt=False,
    strip_formatting=False,
    langs=None,
    forced_title=None,
):
    langs = langs or ["*"]
    ext_exclude = tuple(os.extsep + ext for ext in (EXT, "nfo", "txt"))
    if filename.endswith(ext_exclude) or "-TdarrCacheFile-" in filename:
        print(f"Skipping: {filename}")
        return

    print(f"Processing: {filename}")
    subtitles = ffprobe.subtitles(filename, forced_title)
    if subtitles is None:
        return

    for idx, data in subtitles.items():
        dst = ffprobe.subtitles_path(filename, data)

        if not (
            not data["bitmap"]
            and (forced and data["forced"] or not forced)
            and (skip_srt and data["codec"] != "subrip" or not skip_srt)
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
                "-f",
                "srt",
                "pipe:1",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if proc.returncode != 0:
            print(
                f"FFMPEG error: {filename}: " + proc.stderr.decode(),
                file=sys.stderr,
            )

        elif proc.stdout:
            subs = proc.stdout.decode("latin-1")

            if strip_formatting:
                subs = formatting.strip(subs)

            dst.write_text(subs, encoding="latin-1")
            print(f"Extracted: {dst}")


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        save_subtitles(filename)
