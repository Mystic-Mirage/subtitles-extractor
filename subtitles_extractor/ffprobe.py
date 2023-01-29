import json
import os
import subprocess
import sys
from pathlib import Path
from pprint import pprint

from subtitles_extractor import EXT


def subtitles(filename):
    proc = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_streams",
            "-select_streams",
            "s",
            filename,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        print("FFPROBE error: " + proc.stderr.decode(), file=sys.stderr)
        return None

    result = json.loads(proc.stdout)
    streams = result["streams"]

    data = {}
    for stream in streams:
        try:
            tags = stream["tags"]
            title = tags.get("title", "").lower()
            disposition = stream["disposition"]
            data[stream["index"]] = {
                "language": tags.get("language", "und"),
                "codec": stream["codec_name"],
                "bitmap": "width" in stream,
                "forced": bool(disposition["forced"]) or "forced" in title,
                "sdh": bool(disposition["hearing_impaired"]) or "sdh" in title,
            }
        except KeyError:
            continue

    return data


def subtitles_path(filename, data):
    lang = data["language"]
    sdh = "sdh" if data["sdh"] else None
    forced = "forced" if data["forced"] else None
    parts = ("", lang, sdh, forced, EXT)
    ext = os.extsep.join(part for part in parts if part is not None)
    path = Path(filename).with_suffix(ext)
    return path


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        pprint(subtitles(filename))
